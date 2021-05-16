from datetime import date, timedelta
from core.stock.domain.stock_connector import StockConnector
from core.stock.domain.repository.stock_repository import StockRepository
from core.stock.domain.repository.daily_stock_summary_repository import DailyStockSummaryRepository
from core.stock.domain.stock import Stock
from core.stock.domain.stock_summary import DailyStockSummary


def is_already_crawled(summary: DailyStockSummary):
    if not summary:
        return False
    date = summary.date
    last_working_date = date.today()
    today_weekday = last_working_date.isoweekday()
    SAT = 6
    SUN = 7
    if today_weekday == SAT:
        last_working_date -= timedelta(days=1)
    if today_weekday == SUN:
        last_working_date -= timedelta(days=2)

    return last_working_date <= d


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
        latest_summary = self.daily_stock_summary_repository.find_latest_by_stock(
            stock)
        if is_already_crawled(latest_summary):
            return
        start_date = latest_summary.date if latest_summary else None

        stocks = self.stock_connector.get_daily_stock_summary(
            stock, start_date, end_date)
        self.daily_stock_summary_repository.save_all(stocks)
