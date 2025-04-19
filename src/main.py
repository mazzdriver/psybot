from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, Filters
from handlers import handle_start, handle_help, choose_location, book_slot, confirm_booking, cancel
from config import TELEGRAM_BOT_TOKEN

LOCATION_CHOICE, SLOT_BOOKING = range(2)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("book", choose_location)],  # Первая стадия: выбор локации
    states={
        LOCATION_CHOICE: [MessageHandler(Filters.regex('^(Адрес1|Адрес2|Адрес3)$'), book_slot)],  # Вторая стадия: выбор временного слота
        SLOT_BOOKING: [MessageHandler(Filters.regex('^(Утро|День|Вечер)$'), confirm_booking)]  # Третья стадия: подтверждение бронирования
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

application.add_handler(CommandHandler("start", handle_start))
application.add_handler(CommandHandler("help", handle_help))
application.add_handler(conv_handler)

application.run_polling()