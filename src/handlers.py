# src/handlers.py
from modules import *
from constants import LOCATIONS, SLOTS
from database import Database

router = Router()

class BookingSteps(StatesGroup):
    CHOOSING_LOCATION = State()
    SELECTING_SLOT = State()
    CONFIRMATION = State()

@router.message(Command("start"))
async def handle_start(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать! Нажмите /help для инструкций.")

@router.message(Command("help"))
async def handle_help(message: Message, state: FSMContext):
    await message.answer("/start - запустить бот\n/help - показать справку\n/book - забронировать встречу")

@router.message(Command("book"))
async def handle_book(message: Message, state: FSMContext):
    await state.set_state(BookingSteps.CHOOSING_LOCATION)
    keyboard = [[KeyboardButtonText(text=loc)] for loc in LOCATIONS]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Выберите подходящую вам локацию:", reply_markup=markup)

@router.message(F.text.in_(LOCATIONS))
async def choose_location(message: Message, state: FSMContext):
    await state.set_state(BookingSteps.SELECTING_SLOT)
    selected_location = message.text
    await state.update_data(location=selected_location)
    keyboard = [[KeyboardButtonText(text=slot)] for slot in SLOTS]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Выберите подходящий вам временной слот:", reply_markup=markup)

@router.message(F.text.in_(SLOTS))
async def book_slot(message: Message, state: FSMContext):
    await state.set_state(BookingSteps.CONFIRMATION)
    selected_timeslot = message.text
    data = await state.get_data()
    location = data.get("location")
    db = Database(DATABASE_PATH)
    db.create_tables()
    db.cursor.execute("INSERT INTO bookings(location, timeslot) VALUES (?, ?)", (location, selected_timeslot))
    db.conn.commit()
    db.close_connection()
    await message.answer("Ваше бронирование подтверждено.")

@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено.")

def register_handlers(dp: Dispatcher):
    dp.include_router(router)
    dp.register_states(BookingSteps)  # Регистрация состояний