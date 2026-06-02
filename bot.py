import asyncio
from datetime import datetime
from collections import defaultdict
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ==========================================
# 🔑 ВСТАВЬ СЮДА СВОЙ ТОКЕН ОТ @BotFather
# ==========================================
BOT_TOKEN = "8980489445:AAHO2zKLM5SRT9na4d2qp7TJ6cu1ApLE8ls"

# ==========================================
# ВСЁ, ОСТАЛЬНОЕ НЕ ТРОГАЙ
# ==========================================

# Проверка токена
if not BOT_TOKEN:
    print("❌ ОШИБКА: Вставьте токен в переменную BOT_TOKEN")
    print("📍 Получите токен у @BotFather в Telegram")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

daily_stats = defaultdict(int)
current_date = datetime.now().date()

async def reset_stats_if_needed():
    global daily_stats, current_date
    today = datetime.now().date()
    if today != current_date:
        daily_stats.clear()
        current_date = today

@dp.message()
async def track_activity(message: types.Message):
    await reset_stats_if_needed()
    daily_stats[message.from_user.id] += 1

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
        mention = f"@{username}" if username else f"[Пользователь](tg://user?id={most_active_id})"
    except:
        mention = f"[Пользователь](tg://user?id={most_active_id})"
    
    await message.reply(
        f"🏆 Самый активный сегодня: {mention}\n💬 Сообщений: {max_msgs}",
        parse_mode="Markdown"
    )

async def main():
    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
