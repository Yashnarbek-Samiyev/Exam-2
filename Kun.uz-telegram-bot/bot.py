import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import requests
from bs4 import BeautifulSoup

# Define your Kun.uz URL
KUN_UZ_URL = "https://kun.uz/news/search?q="  # Replace with the actual URL

# Your Telegram bot token
TOKEN = ""

# Define conversation states
KEYWORD = 0


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Welcome to Kun.uz Bot! Please enter a keyword to search for articles.")
    return KEYWORD


def search_articles(update: Update, context: CallbackContext):
    keyword = update.message.text
    url = KUN_UZ_URL + keyword

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('div', class_='news')

        for article in articles[:10]:
            title = article.find('a', class_="news__title").text
            link = article.find('a', class_='news__title')['href']
            article_link = f"https://kun.uz{link}"
            update.message.reply_text(f"{title}\n{article_link}")
    else:
        update.message.reply_text(
            "Failed to retrieve articles. Please try again later.")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            KEYWORD: [MessageHandler(Filters.text & ~Filters.command, search_articles)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
