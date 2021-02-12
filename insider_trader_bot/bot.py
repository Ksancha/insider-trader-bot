import os
import logging
from itertools import islice

from telegram.ext import Updater, CommandHandler

from insider_trader_bot.models import User, UserStocks, Stock
from insider_trader_bot.finviz_connector.functions import get_ticker_transactions, build_ticker_url, get_buy_filtered_transactions, request_ticker
from insider_trader_bot import init_session

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


session = init_session()


def get_transactions(update, context):
    """Get Buy/Sell transactions for a ticker"""
    chat_id = update.message.chat_id
    ticker = context.args[0].upper()
    try:
        transactions = get_ticker_transactions(ticker)
        text = f"Total Buy/Sell According to FinViz: \n" \
               f"Buy: ${transactions['Buy']:,}\n" \
               f"Sell: ${transactions['Sell']:,}\n" \
               f"More info <a href=\"{build_ticker_url(ticker)}\">here</a>"
    except ValueError:
        text = f"Sorry, looks like ticker {ticker} doesn't exist"
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")


def get_top(update, context):
    chat_id = update.message.chat_id
    try:
        top_count = int(context.args[0])
        if top_count < 0:
            raise ValueError
    except (ValueError, IndexError):
        text = "The input should be a positive integer \nTry /top 5 for example ;)"
        context.bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
        return
    try:
        context.bot.send_message(chat_id=chat_id, text="Loading...", parse_mode="HTML")
        output = list(islice(get_buy_filtered_transactions().items(), top_count))
        output = "\n".join([str(x[0]).upper() + " : " + f"${x[1]:,}" for x in output])
        text = f"Top {top_count} companies with recent insider buying activity: \n" + output
    except ValueError:
        text = f"Sorry, something went wrong. Try again later"
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")


def subscribe_to_stock(update, context):
    chat_id = update.message.chat_id
    ticker = context.args[0].upper()
    try:
        request_ticker(ticker)
    except ValueError:
        text = f"Sorry, looks like ticker {ticker} doesn't exist"
        context.bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
        return

    user = _add_user_to_db(username=update.effective_user.username, chat_id=chat_id)
    stock = _add_stock_to_db(ticker=ticker)
    _add_user_stocks_to_db(user=user, stock=stock)


def unsubscribe_from_stock(update, context):
    chat_id = update.message.chat_id
    ticker = context.args[0].upper()
    try:
        request_ticker(ticker)
    except ValueError:
        text = f"Sorry, looks like ticker {ticker} doesn't exist"
        context.bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
        return
    user = session.query(User).filter_by(chat_id=chat_id).first()
    stock = session.query(Stock).filter_by(name=context.args[0].upper()).first()
    if user and stock:
        _remove_user_stock_from_db(user=user, stock=stock)


def list_subscriptions(update, context):
    chat_id = update.message.chat_id
    stocks = session.query(Stock).join(UserStocks).filter(chat_id == UserStocks.user_id).all()
    if not stocks:
        text = "You're not subscribed to any stocks"
    else:
        text = "\n".join([stock.name for stock in stocks])
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")


def main():
    updater = Updater(os.getenv("BOT_SECRET_KEY"), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('get_transactions', get_transactions))
    dp.add_handler(CommandHandler('top', get_top))
    dp.add_handler(CommandHandler('subscribe', subscribe_to_stock))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe_from_stock))
    dp.add_handler(CommandHandler('list_subs', list_subscriptions))
    updater.start_polling()
    updater.idle()


def _add_user_stocks_to_db(user, stock):
    user_stocks = session.query(UserStocks).filter_by(user_id=user.chat_id, stock_id=stock.id).first()
    if user_stocks is None:
        user_stocks = UserStocks(
            user_id=user.chat_id,
            stock_id=stock.id
        )
        session.add(user_stocks)
        session.commit()


def _add_stock_to_db(ticker):
    stock = session.query(Stock).filter_by(name=ticker).first()
    if stock is None:
        stock = Stock(name=ticker)
        session.add(stock)
        session.commit()
    return stock


def _add_user_to_db(username, chat_id):
    user = session.query(User).filter_by(chat_id=chat_id).first()
    if user is None:
        user = User(username=username, chat_id=chat_id)
        session.add(user)
        session.commit()
    return user


def _remove_user_stock_from_db(user, stock):
    user_stocks = session.query(UserStocks).filter_by(user_id=user.chat_id, stock_id=stock.id).first()
    if user_stocks is None:
        return
    session.delete(user_stocks)
    session.commit()


if __name__ == '__main__':
    main()


my_chat_id = 421496653