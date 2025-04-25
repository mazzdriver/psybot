# src/main.py
from modules import *
from config import *
from handlers import register_handlers

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()  # Больше не передается bot

register_handlers(dp)

# Правильная асинхронная обработка
async def main():
    await dp.start_polling(bot)  # Передаем bot в start_polling

if __name__ == "__main__":
    asyncio.run(main())  # Запуск главного асинхронного потока
