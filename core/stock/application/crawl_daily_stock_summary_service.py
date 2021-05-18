from datetime import date, timedelta, datetime
from core.stock.domain.stock_connector import StockConnector
from core.stock.domain.repository.stock_repository import StockRepository
from core.stock.domain.repository.daily_stock_summary_repository import DailyStockSummaryRepository
from core.stock.domain.stock import Stock
from core.stock.domain.stock_summary import DailyStockSummary


def is_already_crawled(latest_date: date):
    if not latest_date:
        return False
    now = datetime.now()
    last_working_date = now.date()
    # Before closing(18 + buffer), crawl until 1 day before
    if now.hour < 19:
        last_working_date -= timedelta(days=1)
    weekday = last_working_date.isoweekday()
    SAT = 6
    SUN = 7
    if weekday == SAT:
        last_working_date -= timedelta(days=1)
    if weekday == SUN:
        last_working_date -= timedelta(days=2)
    return last_working_date <= latest_date


class CrawlDailyStockSummaryService:
    def __init__(self, stock_connector: StockConnector,
                 stock_repository: StockRepository,
                 daily_stock_summary_repository: DailyStockSummaryRepository):
        self.stock_connector = stock_connector
        self.stock_repository = stock_repository
        self.daily_stock_summary_repository = daily_stock_summary_repository

    def crawl_all(self, end_date: date = date.today()):
        for stock in self.stock_repository.find_all():
            self.crawl(stock, end_date)

    def crawl(self, stock: Stock, end_date: date = date.today()):
        latest_summary_date = self.daily_stock_summary_repository.find_latest_date_by_stock(
            stock)
        if is_already_crawled(latest_summary_date):
            return

        start_date = latest_summary_date
        while True:
            stocks, has_next = self.stock_connector.get_daily_stock_summary(
                stock, start_date, end_date)
            self.daily_stock_summary_repository.save_all(stocks)
            if not has_next:
                break
            end_date = stocks[-1].date - timedelta(days=1)
