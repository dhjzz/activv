import os
import asyncio
from datetime import datetime
from collections import defaultdict
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Токен из переменных окружения (настрой на Bothost)
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не найден в переменных окружения")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Статистика
daily_stats = defaultdict(int)
current_date = datetime.now().date()

async def reset_stats_if_needed():
    global daily_stats, current_date
    today = datetime.now().date()
    if today != current_date:
        daily_stats.clear()
        current_date = today

# Считаем все сообщения
@dp.message()
async def track_activity(message: types.Message):
    await reset_stats_if_needed()
    daily_stats[message.from_user.id] += 1
    print(f"Сообщение от {message.from_user.id}, всего: {daily_stats[message.from_user.id]}")

# Команда /activ
@dp.message(Command("activ"))
async def show_activ(message: types.Message):
    await reset_stats_if_needed()
    
    if not daily_stats:
        await message.reply("📭 Сегодня пока нет сообщений.")
        return
    
    most_active_id = max(daily_stats, key=daily_stats.get)
    max_msgs = daily_stats[most_active_id]
    
    try:
        user = await bot.get_chat(most_active_id)
        username = user.username
        if username:
            mention = f"@{username}"
        else:
            mention = f"[Пользователь](tg://user?id={most_active_id})"
    except:
        mention = f"[Пользователь](tg://user?id={most_active_id})"
    
    await message.reply(
        f"🏆 Самый активный сегодня: {mention}\n💬 Сообщений: {max_msgs}",
        parse_mode="Markdown"
    )

# Команда /start (для проверки)
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.reply("✅ Бот работает! Пиши /activ чтобы узнать самого активного.")

# Запуск
async def main():
    print("✅ Бот запущен и работает")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
