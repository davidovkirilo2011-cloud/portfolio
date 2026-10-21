import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# --- МИНИ-ВЕБ-СЕРВЕР ДЛЯ РЕНДЕРА ---
async def handle(request):
    return web.Response(text="Bot is running fine!")

async def start_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- КОД БОТА ---
# Замени ТОВОЙ_ТОКЕН на реальный токен от BotFather
TOKEN = os.environ.get("BOT_TOKEN", "8715722584:AAGEsyupzMyoJcUW2mCwFM4ezeIN6GaMpUc")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я бот для приёма заказов и тикетов. Напиши своё сообщение, и Кирилл скоро ответит!")

async def main():
    # Запускаем сервер портов
    await start_server()
    print("🚀 Бот успешно запущен и готов принимать тикеты!")
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
