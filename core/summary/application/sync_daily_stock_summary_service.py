from datetime import date, timedelta, datetime

from core.stock.domain.repository.stock_repository import StockRepository
from core.stock.domain.stock import Stock
from core.stock.infra.krx.utils import get_last_market_opening_day

from core.summary.domain.repository import DailyStockSummaryRepository
from core.summary.domain.service import FetchDailyStockSummaryService


def get_last_opening_day_has_daily_summary():
    now = datetime.now()
    # 장 마감 이후
    if now.hour < 18:
        now -= timedelta(days=1)
    return get_last_market_opening_day(now.date())


class SyncDailyStockSummaryService:
    def __init__(self,
                 fetch_daily_stock_summary_service: FetchDailyStockSummaryService,
                 stock_repository: StockRepository,
                 daily_stock_summary_repository: DailyStockSummaryRepository):
        self.fetch_daily_stock_summary_service = fetch_daily_stock_summary_service
        self.stock_repository = stock_repository
        self.daily_stock_summary_repository = daily_stock_summary_repository

    def sync_all(self, end_date: date = date.today()):
        last_market_opening_day = get_last_opening_day_has_daily_summary()
        stock_id_latest_date_dic = \
            self.daily_stock_summary_repository.find_latest_dates_by_stock_id()
        stocks = self.stock_repository.find_all()
        total = len(stocks)
        for i, stock in enumerate(stocks):
            yield i, total, stock
            latest_date = stock_id_latest_date_dic.get(stock.id, None)
            if self.__is_already_synced(latest_date, last_market_opening_day):
                continue
            self.sync(stock, latest_date, end_date)

    def sync(self, stock: Stock, start_date: date, end_date: date):
        summaries = self.fetch_daily_stock_summary_service.fetch_all(
            stock.name, stock.code, start_date, end_date)
        self.daily_stock_summary_repository.save_all(summaries)
        end_date = summaries[-1].date - timedelta(days=1)

    def __is_already_synced(self, stock_latest_date, last_market_opening_day):
        return stock_latest_date and last_market_opening_day <= stock_latest_date
