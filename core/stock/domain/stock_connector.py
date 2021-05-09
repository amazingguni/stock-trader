import abc
from datetime import date


class StockConnector(abc.ABC):
    @abc.abstractmethod
    def get_daily_stock(self, stock_code: str, start_date: date, end_date: date):
        raise NotImplementedError
