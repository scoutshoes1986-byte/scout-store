import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# --- НАСТРОЙКИ ---
TOKEN = os.getenv("BOT_TOKEN")  # Токен возьмем из настроек Render
WEBAPP_URL = "https://your-webapp-url.com"  # Ссылка на ваш HTML-сайт (магазин)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ЛОГИКА БОТА ---

@dp.message(CommandStart())
async def start_command(message: types.Message):
    # Красивое приветствие, которое удержит клиента
    text = (
        f"Приветствуем, {message.from_user.first_name}! 👋\n\n"
        "Вы попали в оптовый магазин обуви **ShoesOptom24**.\n"
        "У нас актуальное наличие и самые быстрые отгрузки.\n\n"
        "Нажмите кнопку ниже, чтобы перейти в каталог товаров: 👇"
    )
    
    # Кнопка для открытия Web App
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Открыть каталог", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    
    await message.answer(text, reply_markup=markup, parse_mode="Markdown")

# --- МЕХАНИЗМ "АНТИ-СНА" (ДЛЯ RENDER) ---

async def handle_ping(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render дает порт в переменной окружения PORT
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- ЗАПУСК ---

async def main():
    # Запускаем веб-сервер и бота одновременно
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
