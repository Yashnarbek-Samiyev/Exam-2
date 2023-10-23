

from telegram import Update, KeyboardButtonRequestUser, KeyboardButtonRequestChat
from telegram.ext import Updater, CommandHandler, MessageHandler, filters,  ConversationHandler, CallbackContext
from telegram import ReplyKeyboardMarkup

TOKEN = ''

# Define conversation states
SELECT_OPTION = 0


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id
    first_name = user.first_name
    user_language = user.language_code

    update.message.reply_text(
        f"User ID: {user_id}\nFirst Name: {first_name}\nLanguage: {user_language}")

    keyboard = [
        [KeyboardButtonRequestUser(user_id="User_ID")],
        [KeyboardButtonRequestChat(chat_id="Supergroup_ID")],
        [KeyboardButtonRequestChat(chat_id="Channel_ID")],
        [KeyboardButtonRequestUser(user_id="Bot_ID")],
        [KeyboardButtonRequestChat(chat_id="Group_ID")],
        [KeyboardButtonRequestChat(chat_id="Private_Channel_ID")],
        [KeyboardButtonRequestChat(chat_id="Premium_Selection_ID")]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    update.message.reply_text("Select an option:", reply_markup=reply_markup)

    return SELECT_OPTION


def handle_option(update: Update, context: CallbackContext):
    selected_option = update.message.text

    if selected_option == "User_ID":
        update.message.reply_text("You selected User ID: User_ID")
    elif selected_option == "Supergroup_ID":
        update.message.reply_text("You selected Supergroup ID: Supergroup_ID")
    elif selected_option == "Channel_ID":
        update.message.reply_text("You selected Channel ID: Channel_ID")
    elif selected_option == "Bot_ID":
        update.message.reply_text("You selected Bot ID: Bot_ID")
    elif selected_option == "Group_ID":
        update.message.reply_text("You selected Group ID: Group_ID")
    elif selected_option == "Private_Channel_ID":
        update.message.reply_text(
            "You selected Private Channel ID: Private_Channel_ID")
    elif selected_option == "Premium_Selection_ID":
        update.message.reply_text(
            "You selected Premium Selection ID: Premium_Selection_ID")

    return ConversationHandler.END


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)

    option_handler = MessageHandler(
        filters.text & ~filters.command, handle_option)
    dp.add_handler(option_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
