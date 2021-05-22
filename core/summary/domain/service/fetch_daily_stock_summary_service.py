import abc
from datetime import date


class FetchDailyStockSummaryService:
    @abc.abstractmethod
    def fetch_all(self, stock_code: str, start_date: date, end_date: date):
        raise NotImplementedError
