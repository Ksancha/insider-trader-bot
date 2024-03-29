from insider_trader_bot.models import UserStocks, User, Stock
from insider_trader_bot import session


def _remove_user_stock_from_db(user, stock):
    user_stocks = session.query(UserStocks).filter_by(user_id=user.chat_id, stock_id=stock.id).first()
    if user_stocks is None:
        return
    session.delete(user_stocks)
    session.commit()


def _add_user_to_db(username, chat_id, subscribed_to_buys=False):
    user = session.query(User).filter_by(chat_id=chat_id).first()
    if user is None:
        user = User(username=username, chat_id=chat_id, subscribed_to_buys=subscribed_to_buys)
        session.add(user)
        session.commit()
    return user


def _update_db_user(chat_id, username=None, subscribed_to_buys=False):
    user = session.query(User).filter_by(chat_id=chat_id).first()
    if user is not None:
        if username:
            user.username = username
        if subscribed_to_buys:
            user.subscribed_to_buys = subscribed_to_buys
        session.commit()
    else:
        user = _add_user_to_db(username=username, chat_id=chat_id, subscribed_to_buys=subscribed_to_buys)
    return user


def _add_stock_to_db(ticker):
    stock = session.query(Stock).filter_by(name=ticker).first()
    if stock is None:
        stock = Stock(name=ticker)
        session.add(stock)
        session.commit()
    return stock


def _add_user_stocks_to_db(user, stock):
    user_stocks = session.query(UserStocks).filter_by(user_id=user.chat_id, stock_id=stock.id).first()
    if user_stocks is None:
        user_stocks = UserStocks(
            user_id=user.chat_id,
            stock_id=stock.id
        )
        session.add(user_stocks)
        session.commit()
