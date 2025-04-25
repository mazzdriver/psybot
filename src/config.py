# src/config.py
from modules import load_dotenv, os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('PSYBOT_TOKEN')
DATABASE_PATH = 'data/sqlite.db'
