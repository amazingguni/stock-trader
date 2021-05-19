import abc
from datetime import date

from core.stock.domain.stock import Stock


class StockConnector(abc.ABC):
    @abc.abstractmethod
    def get_account_numbers(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_daily_stock_summary(self, stock: Stock, start_date: date, end_date: date):
        raise NotImplementedError

    @abc.abstractmethod
    def get_account_deposit(self):
        raise NotImplementedError
