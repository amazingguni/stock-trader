from core.stock.domain.repository import StockRepository
from core.summary.domain.repository import DailyStockSummaryRepository


class DeleteDailyStockSummaryService:
    def __init__(self, stock_repository: StockRepository,
                 daily_stock_summary_repository: DailyStockSummaryRepository):
        self.stock_repository = stock_repository
        self.daily_stock_summary_repository = daily_stock_summary_repository

    def delete_all(self, stock_ids):
        for stock_id in stock_ids:
            stock = self.stock_repository.find_by_id(stock_id)
            self.daily_stock_summary_repository.delete_by_stock_code(
                stock.code)
