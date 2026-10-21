import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- МИНИ-ВЕБ-СЕРВЕР ДЛЯ РЕНДЕРА (чтобы сервис был Live) ---
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

# --- КОФИГУРАЦИЯ БОТА ---
TOKEN = os.environ.get("BOT_TOKEN", "8715722584:AAGEsyupzMyoJcUW2mCwFM4ezeIN6GaMpUc")
# Вставь свой Telegram ID (куда бот должен присылать тикеты от клиентов)
ADMIN_ID = 7008254329 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Кнопки клавиатуры
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎫 Создать тикет (Заказ)")],
        [KeyboardButton(text="🌐 Открыть сайт-портфолио")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Привет! Я официальный бот-помощник Кирилла.\n\n"
        "Здесь ты можешь оставить заявку на разработку сайта, лендинга или Telegram-бота.\n"
        "Нажми кнопку ниже или просто напиши своё сообщение сюда!",
        reply_markup=kb
    )

@dp.message(F.text == "🌐 Открыть сайт-портфолио")
async def portfolio_cmd(message: types.Message):
    await message.answer(
        "Посмотреть наши услуги и примеры работ можно на сайте:\n"
        "👉 https://davidovkirilo2011-cloud.github.io/portfolio/"
    )

@dp.message(F.text == "🎫 Создать тикет (Заказ)")
async def ticket_cmd(message: types.Message):
    await message.answer(
        "Напишите суть вашего заказа в одном сообщении (например: «Нужен бот для модерации чата» или «Нужен сайт-визитка»).\n\n"
        "👇 Напишите текст сообщения ниже:"
    )

# Обработка любого другого текста (создание тикета)
@dp.message()
async def process_message(message: types.Message):
    # Уведомляем клиента
    await message.answer("✅ Ваше сообщение получено! Кирилл скоро свяжется с вами.")
    
    # Пересылаем тикет админу
    try:
        user_info = f"📩 **Новый тикет!**\nОт: @{message.from_user.username or 'без_юзернейма'} (ID: {message.from_user.id})\nТекст: {message.text}"
        await bot.send_message(chat_id=ADMIN_ID, text=user_info)
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")

async def main():
    await start_server()
    print("🚀 Бот успешно запущен и готов принимать тикеты!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
