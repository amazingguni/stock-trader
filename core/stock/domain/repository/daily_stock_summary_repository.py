import typing
from core.stock.domain.stock_summary import DailyStockSummary


class DailyStockSummaryRepository:
    def __init__(self):
        pass

    def save(self, stock: DailyStockSummary):
        stock.save()

    def save_all(self, stocks: typing.List[DailyStockSummary]):
        DailyStockSummary.objects.insert(stocks)

    def find_latest_by_stock_code(self, stock_code: str):
        return DailyStockSummary.objects(stock_code=stock_code).order_by('-date').first()
