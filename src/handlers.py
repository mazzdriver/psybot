from telegram import Update
from telegram.ext import CallbackContext
from config import TELEGRAM_BOT_TOKEN
from database import Database

async def handle_start(update: Update, context: CallbackContext):
    await update.message.reply_text("Добро пожаловать! Нажмите /help для инструкций.")

async def handle_help(update: Update, context: CallbackContext):
    await update.message.reply_text("/start - запустить бот\n/help - показать справку\n/book - забронировать встречу")

async def handle_book(update: Update, context: CallbackContext):
    await update.message.reply_text("Процесс бронирования запущен. Выберите дату и время.")