import os
import logging

from telegram.ext import Updater, CommandHandler

from insider_trader_bot.finviz_connector.functions import get_ticker_transactions, build_ticker_url

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def get_transactions(update, context):
    chat_id = update.message.chat_id
    ticker = context.args[0].upper()
    try:
        transactions = get_ticker_transactions(ticker)
        text = f"Total Buy/Sell According to FinViz: \n" \
               f"Buy: {transactions['Buy']:,}$\n" \
               f"Sell: {transactions['Sell']:,}$\n" \
               f"More info <a href=\"{build_ticker_url(ticker)}\">here</a>"
    except ValueError:
        text = f"Sorry, looks like ticker {ticker} doesn't exist"
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")


def main():
    updater = Updater(os.getenv("BOT_SECRET_KEY"), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('get_transactions', get_transactions))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
