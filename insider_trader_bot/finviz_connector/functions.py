import requests
from user_agent import generate_user_agent


from insider_trader_bot.finviz_connector.helpers import get_buy_transactions, get_transaction_records, get_sell_transactions


def get_ticker_transactions(ticker):

    response = requests.get(f"https://finviz.com/quote.ashx?t={ticker}", headers={"User-Agent": generate_user_agent()})

    if response.status_code == 404:
        raise ValueError(f"Invalid ticker {ticker}")

    transactions = get_transaction_records(html_content=response.content, transaction_type=["buy", "sell"])


    buy_transactions = get_buy_transactions(transactions)
    total_buy = get_total_value_amount(buy_transactions)

    sell_transactions = get_sell_transactions(transactions)
    total_sell = get_total_value_amount(sell_transactions)

    return {"Buy": total_buy, "Sell":total_sell}


def get_value_amount(transaction):
    value = int(transaction.contents[-3].next.replace(',', ''))
    return value


def get_total_value_amount(transactions):
    val = 0
    for transaction in transactions:
        val += get_value_amount(transaction)
    return val


# buy_sells = get_ticker_transactions("TSLA")
# pass