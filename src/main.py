import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TELEGRAM_BOT_TOKEN  # Импортируем напрямую
from handlers import router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def main():
    # Инициализация БД (автоматически при создании экземпляра)
    try:
        from database import Database
        Database()  # Просто создаем экземпляр для инициализации
        logger.info("✅ База данных готова")
    except Exception as e:
        logger.critical(f"❌ Ошибка БД: {e}")
        return

    # Создаем бота
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    # Запускаем
    logger.info("🤖 Бот запущен")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("🛑 Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())
