from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup

from constants import LOCATIONS, SLOTS
from database import Database
from config import DATABASE_PATH

router = Router()

class BookingState(StatesGroup):
    location = State()
    time = State()
    fullname = State()

# Общие клавиатуры
def location_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=loc)] for loc in LOCATIONS],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def time_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=time)] for time in SLOTS],
        resize_keyboard=True,
        one_time_keyboard=True
    )

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать! Для записи используйте /book",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Command("book"))
async def start_booking(message: Message, state: FSMContext):
    await state.set_state(BookingState.location)
    await message.answer("Выберите локацию:", reply_markup=location_kb())

@router.message(BookingState.location, F.text.in_(LOCATIONS))
async def process_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(BookingState.time)
    await message.answer("Выберите время:", reply_markup=time_kb())

@router.message(BookingState.time, F.text.in_(SLOTS))
async def process_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(BookingState.fullname)
    await message.answer(
        "Введите ваше имя и фамилию:",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(BookingState.fullname)
async def process_name(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    
    with Database() as db:
        # Сохраняем клиента
        db.execute(
            "INSERT OR IGNORE INTO clients (chat_id) VALUES (?)",
            (message.from_user.id,)
        )
        
        # Получаем ID клиента
        client_id = db.execute(
            "SELECT id FROM clients WHERE chat_id = ?",
            (message.from_user.id,)
        ).fetchone()[0]
        
        # Сохраняем бронирование
        db.execute(
            """INSERT INTO bookings 
            (client_id, location, timeslot) 
            VALUES (?, ?, ?)""",
            (client_id, data['location'], data['time'])
        )
        
    # Отправка психологу
    with Database() as db:
        psychologists = db.execute(
            "SELECT chat_id FROM psychologists"
        ).fetchall()
        
    text = f"Новая запись!\nЛокация: {data['location']}\nВремя: {data['time']}\nКлиент: {message.text}"
    
    for psy in psychologists:
        await bot.send_message(psy[0], text)
    
    await message.answer("✅ Запись оформлена!")
    await state.clear()

@router.message(Command("set_me"))
async def set_psychologist(message: Message):
    with Database() as db:
        db.execute(
            "INSERT OR REPLACE INTO psychologists (chat_id) VALUES (?)",
            (message.from_user.id,)
        )
    await message.answer("✅ Вы назначены психологом!")