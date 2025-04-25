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

@router.message(F.text.in_(LOCATIONS))
async def choose_location(message: Message, state: FSMContext):
    await state.set_state(BookingSteps.CHOOSE_LOCATION)
    keyboard = [[KeyboardButton(loc)] for loc in LOCATIONS]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Выберите подходящую вам локацию:", reply_markup=markup)

@router.message(F.text.in_(SLOTS))
async def book_slot(message: Message, state: FSMContext):
    await state.set_state(BookingSteps.SELECT_SLOT)
    selected_location = message.text
    await state.update_data(location=selected_location)
    keyboard = [[KeyboardButton(slot)] for slot in SLOTS]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Выберите подходящий вам временной слот:", reply_markup=markup)

@router.message(StateFilter(BookingSteps.CONFIRMATION))
async def confirm_booking(message: Message, state: FSMContext):
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