# Импортируем необходимые библиотеки
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters
)
from dotenv import load_dotenv
import os
import logging

# Настраиваем логирование
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s]: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка токена из .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Основная логика бота
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатываем команду /start."""
    user = update.effective_user
    logger.info(f"{user.first_name} запустил бота.")
    await update.message.reply_text("Привет, я бот-записывалка!")

async def handle_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Простое эхо-сообщение."""
    message = update.message.text
    logger.info(f"Сообщение от {update.effective_user.first_name}: {message}")
    await update.message.reply_text("Helloworld")

def main():
    # Создание приложения
    app = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", handle_start))      # Команда /start
    app.add_handler(MessageHandler(filters.ALL, handle_echo))   # Все остальные сообщения

    # Запуск бота
    try:
        print("Запускаю бота...")
        app.run_polling()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    main().