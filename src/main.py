from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import handle_start, handle_help, handle_book
from config import TELEGRAM_BOT_TOKEN

application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

application.add_handler(CommandHandler("start", handle_start))
application.add_handler(CommandHandler("help", handle_help))
application.add_handler(CommandHandler("book", handle_book))

application.run_polling()