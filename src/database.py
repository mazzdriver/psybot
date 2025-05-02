import sqlite3
from contextlib import contextmanager
from config import DATABASE_PATH  # Импортируем напрямую

class Database:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def get_cursor(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Доступ к полям по имени
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _init_db(self):
        """Создаем таблицы при первом запуске"""
        with self.get_cursor() as c:
            # Психологи
            c.execute('''CREATE TABLE IF NOT EXISTS psychologists (
                       chat_id INTEGER PRIMARY KEY
                   )''')
            
            # Клиенты
            c.execute('''CREATE TABLE IF NOT EXISTS clients (
                       chat_id INTEGER PRIMARY KEY,
                       fullname TEXT
                   )''')
            
            # Бронирования
            c.execute('''CREATE TABLE IF NOT EXISTS bookings (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       client_id INTEGER,
                       location TEXT,
                       timeslot TEXT,
                       FOREIGN KEY(client_id) REFERENCES clients(chat_id)
                   )''')
