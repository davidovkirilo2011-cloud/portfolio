import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

# Твой токен от BotFather
BOT_TOKEN = "8715722584:AAGEsyupzMyoJcUW2mCwFM4ezeIN6GaMpUc"

# Твой реальный Telegram ID
ADMIN_ID = 7008254329

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class TicketState(StatesGroup):
    waiting_for_task = State()


def main_keyboard():
    kb = [
        [KeyboardButton(text="🎫 Создать тикет (Заказ)")],
        [KeyboardButton(text="🌐 Открыть сайт-портфолио")],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        f"Добро пожаловать в сервис заказа сайтов и Telegram-ботов.\n"
        f"Чтобы оставить заявку или задать вопрос, нажми кнопку 'Создать тикет' ниже!",
        reply_markup=main_keyboard(),
    )


@dp.message(F.text == "🌐 Открыть сайт-портфолио")
async def send_website(message: types.Message):
    await message.answer(
        "Посмотреть наши услуги и примеры работ можно на сайте:\n"
        "👉 https://davidovkirilo2011-cloud.github.io/portfolio/"
    )


@dp.message(F.text == "🎫 Создать тикет (Заказ)")
async def start_ticket(message: types.Message, state: FSMContext):
    await state.set_state(TicketState.waiting_for_task)
    await message.answer(
        "📝 Опишите вашу задачу:\n\n"
        "Например: «Нужен сайт-визитка для сервиса ремонта телефонов» или «Нужен бот для модерации чата».\n\n"
        "Напишите текст сообщения ниже 👇"
    )


@dp.message(TicketState.waiting_for_task)
async def process_ticket(message: types.Message, state: FSMContext):
    task_text = message.text
    user = message.from_user
    username = f"@{user.username}" if user.username else "нет юзернейма"

    # Ответ клиенту
    await message.answer(
        "✅ Ваш тикет успешно создан!\nМы свяжемся с вами в ближайшее время.",
        reply_markup=main_keyboard(),
    )

    # Сообщение тебе (админу)
    ticket_for_admin = (
        f"📥 НОВЫЙ ТИКЕТ (ЗАКАЗ)!\n\n"
        f"👤 Заказчик: {user.first_name} ({username})\n"
        f"🆔 ID: {user.id}\n\n"
        f"💬 Описание задачи:\n{task_text}"
    )

    try:
        await bot.send_message(chat_id=ADMIN_ID, text=ticket_for_admin)
    except Exception as e:
        print(f"Ошибка отправки тикета админу: {e}")

    await state.clear()


async def main():
    print("🚀 Бот успешно запущен и готов принимать тикеты!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
