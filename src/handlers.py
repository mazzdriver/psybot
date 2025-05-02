from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup

from database import Database
from constants import LOCATIONS, SLOTS

router = Router()

class BookingState(StatesGroup):
    location = State()
    time = State()
    fullname = State()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Добро пожаловать! Для записи используйте /book")

@router.message(Command("book"))
async def start_booking(message: Message, state: FSMContext):
    await state.set_state(BookingState.location)
    await message.answer(
        "Выберите локацию:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=loc)] for loc in LOCATIONS],
            resize_keyboard=True
        )
    )

@router.message(Command("my_bookings"))
async def show_bookings(message: Message):
    db = Database()
    try:
        with db.get_cursor() as cursor:
            # Проверяем, является ли пользователь психологом
            cursor.execute(
                "SELECT 1 FROM psychologists WHERE chat_id = ?",
                (message.from_user.id,)
            )
            if not cursor.fetchone():
                await message.answer("❌ Вы не зарегистрированы как психолог")
                return

            # Получаем все записи
            cursor.execute('''
                SELECT b.location, b.timeslot, c.fullname 
                FROM bookings b
                JOIN clients c ON b.client_id = c.chat_id
                ORDER BY b.timeslot
            ''')
            bookings = cursor.fetchall()

        if not bookings:
            await message.answer("📭 У вас нет записей")
            return

        response = ["📅 Ваши записи:"]
        for booking in bookings:
            response.append(
                f"▪ {booking['timeslot']} - {booking['fullname']} ({booking['location']})"
            )
        
        await message.answer("\n".join(response))
        
    except Exception as e:
        await message.answer("⚠️ Ошибка при получении записей")
        print(f"Database error: {e}")


@router.message(BookingState.location, F.text.in_(LOCATIONS))
async def process_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(BookingState.time)
    await message.answer(
        "Выберите время:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=time)] for time in SLOTS],
            resize_keyboard=True
        )
    )

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
    db = Database()
    
    try:
        with db.get_cursor() as cursor:
            # Сохраняем клиента
            cursor.execute(
                "INSERT OR IGNORE INTO clients (chat_id, fullname) VALUES (?, ?)",
                (message.from_user.id, message.text)
            )
            
            # Сохраняем бронирование
            cursor.execute(
                """INSERT INTO bookings
                (client_id, location, timeslot)
                VALUES (?, ?, ?)""",
                (message.from_user.id, data['location'], data['time'])
            )
            
            # Получаем психологов
            cursor.execute("SELECT chat_id FROM psychologists")
            psychologists = cursor.fetchall()
            
        # Отправляем уведомления
        text = f"Новая запись!\nЛокация: {data['location']}\nВремя: {data['time']}\nКлиент: {message.text}"
        for psy in psychologists:
            await bot.send_message(psy['chat_id'], text)
            
        await message.answer("✅ Запись оформлена!")
        
    except Exception as e:
        await message.answer("⚠️ Произошла ошибка при записи. Пожалуйста, попробуйте позже.")
        print(f"Database error: {e}")
    
    await state.clear()

@router.message(Command("set_me"))
async def set_psychologist(message: Message):
    db = Database()
    try:
        with db.get_cursor() as cursor:
            cursor.execute(
                "INSERT OR REPLACE INTO psychologists (chat_id) VALUES (?)",
                (message.from_user.id,)
            )
        await message.answer("✅ Вы назначены психологом!")
    except Exception as e:
        await message.answer("⚠️ Не удалось сохранить данные.")
        print(f"Database error: {e}")
