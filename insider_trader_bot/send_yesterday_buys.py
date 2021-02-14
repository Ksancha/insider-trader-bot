from telegram import Bot
from datetime import date, timedelta
from itertools import islice
import os

from insider_trader_bot import session
import insider_trader_bot.finviz_connector.functions as finviz_fnc
from insider_trader_bot.models import User


def send_yesterday_buys():
    bot = Bot(token=os.getenv("BOT_SECRET_KEY"))
    # t2 = datetime.strptime("2021-02-13 00:00:00", "%Y-%m-%d %H:%M:%S").date()
    t2 = date.today()
    t1 = t2 - timedelta(days=1)
    yesterday_buys = finviz_fnc.get_timerange_buy_transactions(t1=t1, t2=t2)
    if yesterday_buys:
        output = list(islice(yesterday_buys.items(), 10))
        output = "\n".join([finviz_fnc.build_ticker_href(str(x[0]).upper()) + " : " + f"${x[1]:,}" for x in output])
        text = f"Top 10 companies with insider buying activity on {t1}: \n" + output
        for user in session.query(User).filter(User.subscribed_to_buys == 1).all():
            bot.send_message(chat_id=user.chat_id, text=text, parse_mode="HTML")


if __name__ == "__main__":
    send_yesterday_buys()
