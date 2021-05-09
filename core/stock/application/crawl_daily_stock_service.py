from datetime import date
from core.stock.domain.stock_connector import StockConnector
from core.stock.domain.repository.daily_stock_summary_repository import DailyStockSummaryRepository


class CrawlDailyStockService:
    def __init__(self, stock_connector: StockConnector,
                 daily_stock_summary_repository: DailyStockSummaryRepository):
        self.stock_connector = stock_connector
        self.daily_stock_summary_repository = daily_stock_summary_repository

    def crawl(self, stock_code: str, end_date: date = date.today()):
        latest_stock = self.daily_stock_summary_repository.find_latest_by_stock_code(
            stock_code)
        start_date = latest_stock.date if latest_stock else None
        stocks = self.stock_connector.get_daily_stock_summary(
            stock_code, start_date, end_date)
        self.daily_stock_summary_repository.save_all(stocks)
