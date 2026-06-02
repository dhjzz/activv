import os
import asyncio
from datetime import datetime
from collections import defaultdict
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Токен из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не найден")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Статистика
daily_stats = defaultdict(int)
current_date = datetime.now().date()

async def reset_stats():
    global daily_stats, current_date
    today = datetime.now().date()
    if today != current_date:
        daily_stats.clear()
        current_date = today
        print(f"📅 Статистика обнулена: {today}")

# Обработка ВСЕХ сообщений
@dp.message()
async def handle_all_messages(message: types.Message):
    await reset_stats()
    user_id = message.from_user.id
    daily_stats[user_id] += 1
    print(f"📊 {user_id}: {daily_stats[user_id]}")

# Команда /activ
@dp.message(Command("activ"))
async def cmd_activ(message: types.Message):
    await reset_stats()
    
    if not daily_stats:
        await message.answer("📭 Сегодня ещё никто не писал!")
        return
    
    # Находим самого активного
    top_user = max(daily_stats, key=daily_stats.get)
    count = daily_stats[top_user]
    
    # Получаем инфо о пользователе
    try:
        chat = await bot.get_chat(top_user)
        name = chat.username or f"user{top_user}"
        mention = f"@{name}" if chat.username else f"[Пользователь](tg://user?id={top_user})"
    except:
        mention = f"[Пользователь](tg://user?id={top_user})"
    
    await message.answer(
        f"🏆 **Самый активный сегодня:**\n{mention}\n📊 **Сообщений:** {count}",
        parse_mode="Markdown"
    )

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "✅ Бот работает!\n\n"
        "📌 Команды:\n"
        "/activ - кто сегодня самый активный\n"
        "/start - показать это сообщение"
    )

# Запуск
async def main():
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
