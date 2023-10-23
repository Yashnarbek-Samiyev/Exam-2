import logging
from typing import Dict
from db import get_category_all, get_category_id_by_name, get_category_product
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


logger = logging.getLogger(__name__)

CAT_CHOOSING, PRODUCT, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['☎️ Biz bilan aloqa', '🛍 Buyurtma berish'],
    ['✍️ Fikr bildirish', '⚙️ Sozlamalar'],
]
main_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Davom etamizmi? 😉",
        reply_markup=main_markup,
    )
    return ConversationHandler.END


def category(update: Update, context: CallbackContext) -> int:
    categories = get_category_all()
    categories_keyboard = []
    for i in range(0, len(categories), 2):

        categories_keyboard.append(
            [cat.title for cat in categories[i:i+2]],
        )
    categories_keyboard.insert(0, ["📥Savatcha"])
    categories_keyboard.append(["🔙Back To Menu"])
    categories_markup = ReplyKeyboardMarkup(
        categories_keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Kerakli kategoriyani tanlang:",
        reply_markup=categories_markup,
    )

    return CAT_CHOOSING


def cat_choosing(update: Update, context: CallbackContext) -> int:
    category = get_category_id_by_name(update.message.text)
    if category:

        products = get_category_product(category.id)
        products_keyboard = []
        for i in range(0, len(products), 2):

            products_keyboard.append(
                [product.title for product in products[i:i+2]],

            )
        products_keyboard.insert(0, ["📥Savatcha"])
        products_keyboard.append(["🔙Back"])
        products_markup = ReplyKeyboardMarkup(
            products_keyboard, resize_keyboard=True)
        update.message.reply_text(
            "Kerakli mahsulotni tanlang.",
            reply_markup=products_markup,
        )
        return PRODUCT
    else:
        categories = get_category_all()

        categories_keyboard = []
        for i in range(0, len(categories), 2):

            categories_keyboard.append(
                [cat.title for cat in categories[i:i+2]]
            )
        categories_keyboard.insert(0, ["📥Savatcha"])
        categories_keyboard.append(["🔙Back To Menu"])
        categories_markup = ReplyKeyboardMarkup(
            categories_keyboard, resize_keyboard=True)
        update.message.reply_text(
            "unday kategoriya mavjud emas, Kerakli kategoriyani tanlang:",
            reply_markup=categories_markup,
        )

        return CAT_CHOOSING


def product(update: Update, context: CallbackContext) -> int:
    category = get_category_product(update.message.text)
    if category:
        update.message.reply_text(
            category.id,
        )

    else:
        categories = get_category_all()

        categories_keyboard = []
        for i in range(0, len(categories), 2):

            categories_keyboard.append(
                [],
                [cat.title for cat in categories[i:i+2]],
                []
            )
        categories_keyboard.insert(0, ["📥Savatcha"])
        categories_keyboard.append(["🔙Back To Menu"])
        categories_markup = ReplyKeyboardMarkup(
            categories_keyboard, resize_keyboard=True)
        update.message.reply_text(
            "unday kategoriya mavjud emas, Kerakli kategoriyani tanlang:",
            reply_markup=categories_markup,
        )

        return CAT_CHOOSING


def main() -> None:
    """Run the bot."""
    updater = Updater("")

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(Filters.text("🛍 Buyurtma berish"), category),
            MessageHandler(Filters.text("🔙Back"), product),


        ],
        states={
            CAT_CHOOSING: [
                MessageHandler(
                    Filters.text & ~Filters.command, cat_choosing
                ),
                MessageHandler(Filters.text("🔙Back To Menu")
                               & ~Filters.command, start)


            ],
            PRODUCT: [
                MessageHandler(
                    Filters.text & ~Filters.command, product
                ),
                MessageHandler(Filters.text("🔙Back") & ~
                               Filters.command, cat_choosing),


            ],

        },
        fallbacks=[
            CommandHandler('start', start),
            MessageHandler(Filters.text("🛍 Buyurtma berish"), category),
            MessageHandler(Filters.text("🔙Back"), product),

        ],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
