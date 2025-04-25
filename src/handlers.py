# src/handlers.py
from modules import *
from constants import LOCATIONS, SLOTS
from config import TELEGRAM_BOT_TOKEN
from database import Database

async def handle_start(update: types.Update, context: types.CallbackContext):
    await update.message.reply_text("Добро пожаловать! Нажмите /help для инструкций.")

async def handle_help(update: types.Update, context: types.CallbackContext):
    await update.message.reply_text("/start - запустить бот\n/help - показать справку\n/book - забронировать встречу")

async def choose_location(update: types.Update, context: types.CallbackContext):
    keyboard = [[KeyboardButton(loc)] for loc in LOCATIONS]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Выберите подходящую вам локацию:", reply_markup=markup)

async def book_slot(update: types.Update, context: types.CallbackContext):
    selected_location = update.message.text
    context.user_data["location"] = selected_location
    keyboard = [[KeyboardButton(slot)] for slot in SLOTS]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Выберите подходящий вам временной слот:", reply_markup=markup)

async def confirm_booking(update: types.Update, context: types.CallbackContext):
    selected_timeslot = update.message.text
    location = context.user_data.get("location")
    db = Database(DATABASE_PATH)
    db.create_tables()
    db.cursor.execute("INSERT INTO bookings(location, timeslot) VALUES (?, ?)", (location, selected_timeslot))
    db.conn.commit()
    db.close_connection()
    await update.message.reply_text("Ваше бронирование подтверждено.")

async def cancel(update: types.Update, context: types.CallbackContext):
    await update.message.reply_text("Действие отменено.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(handle_start, commands=["start"])
    dp.register_message_handler(handle_help, commands=["help"])
    dp.register_message_handler(choose_location, text=LOCATIONS)
    dp.register_message_handler(book_slot, text=SLOTS)
    dp.register_message_handler(confirm_booking, state="booking_confirmation")
    dp.register_message_handler(cancel, commands=["cancel"])
    