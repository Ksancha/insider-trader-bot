from unittest import TestCase

import datetime
from insider_trader_bot.finviz_connector.objects import sec_date_to_datetime


class TestSecToDateTime(TestCase):

    def test_sec_date_same_year(self):
        sec_date = "Feb 09 07:56 PM"
        today = datetime.datetime.strptime("2021-02-10 00:00:00", "%Y-%m-%d %H:%M:%S")
        sec_date_datetime = sec_date_to_datetime(sec_date, today)

        expected = datetime.datetime.strptime("2021-02-09 19:56:00", "%Y-%m-%d %H:%M:%S")
        self.assertEqual(sec_date_datetime, expected)

    def test_sec_date_last_year(self):
        sec_date = "Dec 09 07:56 PM"
        today = datetime.datetime.strptime("2021-02-10 00:00:00", "%Y-%m-%d %H:%M:%S")
        sec_date_datetime = sec_date_to_datetime(sec_date, today)

        expected = datetime.datetime.strptime("2020-12-09 19:56:00", "%Y-%m-%d %H:%M:%S")
        self.assertEqual(sec_date_datetime, expected)

    def test_sec_date_last_year_same_month(self):
        sec_date = "Feb 11 07:56 PM"
        today = datetime.datetime.strptime("2021-02-10 00:00:00", "%Y-%m-%d %H:%M:%S")
        sec_date_datetime = sec_date_to_datetime(sec_date, today)

        expected = datetime.datetime.strptime("2020-02-11 19:56:00", "%Y-%m-%d %H:%M:%S")
        self.assertEqual(sec_date_datetime, expected)
