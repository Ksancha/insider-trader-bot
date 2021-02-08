import os

from telegram.ext import Updater, CommandHandler

from insider_trader_bot.finviz_connector.functions import get_ticker_transactions


def get_transactions(update, context):
    chat_id = update.message.chat_id
    ticker = context.args[0].upper()
    try:
        transactions = get_ticker_transactions(ticker)
        text = f"Total Buy/Sell According to FinViz: \n" \
               f"Buy: {transactions['Buy']:,}" + "$\n" \
               f"Sell: {transactions['Sell']:,}" + "$"
    except ValueError:
        text = f"Sorry, looks like ticker {ticker} doesn't exist"
    context.bot.send_message(chat_id=chat_id, text=text)


def main():
    updater = Updater(os.getenv("BOT_SECRET_KEY"), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('get_transactions', get_transactions))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
