import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# --- НАСТРОЙКИ ---
# Токен мы впишем на самом сайте Render, в коде его НЕ ПИШЕМ!
TOKEN = os.getenv("BOT_TOKEN") 
# Сюда можно будет вставить ссылку на твой магазин позже
WEBAPP_URL = "https://google.com" 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ЧТО ВИДИТ КЛИЕНТ ПРИ СТАРТЕ ---
@dp.message(CommandStart())
async def start_command(message: types.Message):
    text = (
        f"Приветствуем, {message.from_user.first_name}! 👋\n\n"
        "Вы попали в оптовый магазин обуви **ShoesOptom24**.\n\n"
        "Нажмите кнопку ниже, чтобы открыть каталог: 👇"
    )
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Открыть каталог", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    
    await message.answer(text, reply_markup=markup, parse_mode="Markdown")

# --- БЛОК ДЛЯ RENDER (ЧТОБЫ БОТ НЕ СПАЛ) ---
async def handle_ping(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- ЗАПУСК ---
async def main():
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
