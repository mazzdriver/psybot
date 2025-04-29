import sqlite3
from contextlib import contextmanager
from config import DATABASE_PATH

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
    
    def __enter__(self):
        return self.conn.cursor()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()
    @contextmanager
    def get_cursor(self):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            conn.close()

    def init_db(self):
        with self.get_cursor() as c:
            # Таблица психологов
            c.execute('''CREATE TABLE IF NOT EXISTS psychologists (
                        chat_id INTEGER PRIMARY KEY
                    )''')
            
            # Таблица клиентов
            c.execute('''CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chat_id INTEGER,
                        first_name TEXT,
                        last_name TEXT,
                        UNIQUE(chat_id)
                    )''')
            
            # Бронирования
            c.execute('''CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_id INTEGER REFERENCES clients(id),
                        location TEXT,
                        timeslot TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
