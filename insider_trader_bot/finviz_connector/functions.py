import requests
from collections import defaultdict
from user_agent import generate_user_agent


from insider_trader_bot.finviz_connector.helpers import get_buy_transactions, get_transaction_records, get_sell_transactions, get_all_buy_transactions
from insider_trader_bot.finviz_connector.objects import Transactions


def get_ticker_transactions(ticker):

    response = request_ticker(ticker)

    transactions = get_transaction_records(html_content=response.content, transaction_type=["buy", "sell"])

    buy_transactions = get_buy_transactions(transactions)
    total_buy = get_total_value_amount(buy_transactions)

    sell_transactions = get_sell_transactions(transactions)
    total_sell = get_total_value_amount(sell_transactions)

    return {"Buy": total_buy, "Sell": total_sell}


def request_ticker(ticker):
    response = requests.get(build_ticker_url(ticker), headers={"User-Agent": generate_user_agent()})

    if response.status_code == 404:
        raise ValueError(f"Invalid ticker {ticker}")
    return response


def build_ticker_href(ticker):
    return f'<a href="https://finviz.com/quote.ashx?t={ticker}">{ticker}</a>'


def build_ticker_url(ticker):
    return f"https://finviz.com/quote.ashx?t={ticker}"


def get_value_amount(transaction):
    value = int(transaction.contents[-3].next.replace(',', ''))
    return value


def get_total_value_amount(transactions):
    val = 0
    for transaction in transactions:
        val += get_value_amount(transaction)
    return val


def get_all_insider_buy_page():
    return requests.get("https://finviz.com/insidertrading.ashx?tc=1", headers={"User-Agent": generate_user_agent()})


def filter_transactions(transactions, min_val, ticker=None):
    output = []
    for tr in [Transactions.from_finviz_html_obj(t) for t in transactions]:
        if ticker:
            if tr.ticker == ticker.lower() and tr.value > min_val:
                output.append(tr)
        elif tr.value > min_val:
            output.append(tr)
    return output


def _group_by_ticker(transactions):
    output = defaultdict(list)
    for tr in transactions:
        output[tr.ticker].append(tr)
    return output


def get_buy_filtered_transactions(min_val=0, ticker=None):
    response = get_all_insider_buy_page()

    if response.status_code == 404:
        raise ValueError(f"Could not access FinViz URL")
    transactions = get_all_buy_transactions(response.content)
    filtered_transactions = filter_transactions(transactions=transactions, min_val=min_val, ticker=ticker)
    filtered_transactions = _group_by_ticker(filtered_transactions)
    output = {}
    for k in filtered_transactions.keys():
        output[k] = sum(tr.value for tr in filtered_transactions[k])
    return {k: v for k, v in sorted(output.items(), key=lambda item: item[1], reverse=True)}

