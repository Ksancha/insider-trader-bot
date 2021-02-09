

class Transactions:

    def __init__(
            self,
            ticker,
            owner,
            relationship,
            transaction_type,
            cost,
            number_of_shares,
            value,
            sec_date,
            date=None,
            shares_total=None
    ):
        self.ticker = ticker.lower()
        self.owner = owner
        self.relationship = relationship
        self.transaction_type = transaction_type.lower()
        self.cost = cost
        self.number_of_shares = number_of_shares
        self.value = value
        self.number_of_shares = number_of_shares
        self.sec_date = sec_date
        self.date = date
        self.shares_total = shares_total

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        try:
            self._value = int(val)
        except ValueError:
            self._value = int(val.replace(",", ""))

    @classmethod
    def from_finviz_html_obj(cls, html_obj, ticker_included=True, ticker=None):
        if ticker_included:
            return cls(
                ticker=html_obj.contents[0].next.next,
                owner=html_obj.contents[1].next.next,
                relationship=html_obj.contents[2].next,
                date=html_obj.contents[3].next,
                transaction_type=html_obj.contents[4].next,
                cost=html_obj.contents[5].next,
                number_of_shares=html_obj.contents[6].next,
                value=html_obj.contents[7].next,
                shares_total=html_obj.contents[8].next,
                sec_date=html_obj.contents[9].next.next,
            )
        else:
            return cls(
                ticker=ticker,
                owner=html_obj.contents[0].next.next,
                relationship=html_obj.contents[1].next,
                date=html_obj.contents[2].next,
                transaction_type=html_obj.contents[3].next,
                cost=html_obj.contents[4].next,
                number_of_shares=html_obj.contents[5].next,
                value=html_obj.contents[6].next,
                shares_total=html_obj.contents[7].next,
                sec_date=html_obj.contents[8].next.next,
            )

    def __add__(self, other):
        if self.transaction_type == other.transaction_type and self.ticker == other.ticker:
            return self.value + other.value
        else:
            raise ValueError("Trying to add different transaction types")
