from datetime import date, timedelta, datetime

from core.stock.domain.stock_connector import StockConnector
from core.stock.domain.repository.stock_repository import StockRepository
from core.stock.domain.repository.daily_stock_summary_repository import DailyStockSummaryRepository
from core.stock.domain.stock import Stock

from core.stock.infra.krx.utils import get_last_market_opening_day


def get_last_opening_day_has_daily_summary():
    now = datetime.now()
    # 장 마감 이후
    if now.hour < 18:
        now -= timedelta(days=1)
    return get_last_market_opening_day(now.date())


class CrawlDailyStockSummaryService:
    def __init__(self, stock_connector: StockConnector,
                 stock_repository: StockRepository,
                 daily_stock_summary_repository: DailyStockSummaryRepository):
        self.stock_connector = stock_connector
        self.stock_repository = stock_repository
        self.daily_stock_summary_repository = daily_stock_summary_repository

    def crawl_all(self, end_date: date = date.today()):
        last_market_opening_day = get_last_opening_day_has_daily_summary()
        stock_id_latest_date_dic = \
            self.daily_stock_summary_repository.find_latest_dates_by_stock_id()
        stocks = self.stock_repository.find_all()
        total = len(stocks)
        for i, stock in enumerate(stocks):
            yield i, total, stock
            latest_date = stock_id_latest_date_dic.get(stock.id, None)
            if self.__is_already_crawled(latest_date, last_market_opening_day):
                continue
            self.crawl(stock, latest_date, end_date)

    def crawl(self, stock: Stock, start_date: date, end_date: date):
        while True:
            stocks, has_next = self.stock_connector.get_daily_stock_summary(
                stock, start_date, end_date)
            self.daily_stock_summary_repository.save_all(stocks)
            if not has_next:
                break
            end_date = stocks[-1].date - timedelta(days=1)

    def __is_already_crawled(self, stock_latest_date, last_market_opening_day):
        return stock_latest_date and last_market_opening_day <= stock_latest_date
