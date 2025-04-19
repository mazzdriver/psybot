from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('PSYBOT_TOKEN')
DATABASE_PATH = 'data/sqlite.db'