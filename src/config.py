import os
from pathlib import Path
from dotenv import load_dotenv

# Создаем папку для БД если её нет
Path("data").mkdir(exist_ok=True)

# Загружаем переменные окружения
load_dotenv()

# Настройки
TELEGRAM_BOT_TOKEN = os.getenv("PSYBOT_TOKEN")
DATABASE_PATH = "data/sqlite.db"

# Валидация
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ Токен бота не найден! Проверьте .env файл")
