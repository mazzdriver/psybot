from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from config import TELEGRAM_BOT_TOKEN
from database import Database

LOCATIONS = ["Адрес1", "Адрес2", "Адрес3"]  # Списки локаций
SLOTS = ["Утро", "День", "Вечер"]  # Временные слоты

async def handle_start(update: Update, context: CallbackContext):
    await update.message.reply_text("Добро пожаловать! Нажмите /help для инструкций.")

async def handle_help(update: Update, context: CallbackContext):
    await update.message.reply_text("/start - запустить бот\n/help - показать справку\n/book - забронировать встречу")

async def choose_location(update: Update, context: CallbackContext):
    """
    Показывает пользователю список локаций для выбора.
    """
    keyboard = [[KeyboardButton(loc)] for loc in LOCATIONS]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Выберите подходящую вам локацию:", reply_markup=markup)

async def book_slot(update: Update, context: CallbackContext):
    """
    После выбора локации показывает доступные временные слоты.
    """
    selected_location = update.message.text
    context.user_data["location"] = selected_location
    keyboard = [[KeyboardButton(slot)] for slot in SLOTS]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Выберите подходящий вам временной слот:", reply_markup=markup)

async def confirm_booking(update: Update, context: CallbackContext):
    """
    Завершает процедуру бронирования, сохраняет данные в базу.
    """
    selected_timeslot = update.message.text
    location = context.user_data.get("location")  # Берём локацию из контекста
    db = Database(DATABASE_PATH)
    db.create_tables()
    db.cursor.execute("INSERT INTO bookings(location, timeslot) VALUES (?, ?)", (location, selected_timeslot))
    db.conn.commit()
    db.close_connection()
    await update.message.reply_text("Ваше бронирование подтверждено.")

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Действие отменено.")