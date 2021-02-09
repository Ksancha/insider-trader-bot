from bs4 import BeautifulSoup


def get_transaction_records(html_content, transaction_type=None):
    """Get transaction records from Finviz page filter by transaction type if provided"""
    soup = BeautifulSoup(html_content, 'html.parser')
    table_rows = soup.find_all(lambda tag: tag.name == "tr" and len(tag.contents) == 9)
    transaction_rows = []
    output = []
    for row in table_rows:
        if row.attrs.get("class", ["_"])[0].startswith("insider"):
            transaction_rows.append(row)
    if transaction_type is None:
        return transaction_rows
    if "buy" in transaction_type or transaction_type == "buy":
        output.extend(get_buy_transactions(transaction_rows))
    if "sell" in transaction_type or transaction_type == "sell":
        output.extend(get_sell_transactions(transaction_rows))
    return output


def is_buy_transaction(transaction):
    """Check whether the transaction is Buy"""
    try:
        return transaction.contents[3].next == "Buy"
    except IndexError:
        return False


def get_buy_transactions(transactions):
    """Filter buy transactions from all transactions list"""
    buy_transactions = [transaction for transaction in transactions if is_buy_transaction(transaction)]
    return buy_transactions


def is_sell_transaction(transaction):
    """Check whether the transaction is Sale"""
    try:
        return transaction.contents[3].next == "Sale"
    except IndexError:
        return False


def get_sell_transactions(transactions):
    """Filter sell transactions from all transactions list"""
    sell_transactions = [transaction for transaction in transactions if is_sell_transaction(transaction)]
    return sell_transactions


def get_value_amount(transaction):
    value = int(transaction.contents[-3].next.replace(',', ''))
    return value


def get_total_buy_amount(transactions):
    val = 0
    for transaction in transactions:
        val += get_value_amount(transaction)
    return val


def get_all_buy_transactions(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    transactions = soup.find_all(lambda tag: tag.name == "tr" and len(tag.contents) == 10)
    return transactions
