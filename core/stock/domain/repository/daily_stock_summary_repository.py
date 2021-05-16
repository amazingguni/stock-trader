import typing
from core.stock.domain.stock_summary import DailyStockSummary
from core.stock.domain.stock import Stock


class DailyStockSummaryRepository:
    def __init__(self):
        pass

    def save(self, stock: DailyStockSummary):
        stock.save()

    def save_all(self, stocks: typing.List[DailyStockSummary]):
        if stocks:
            DailyStockSummary.objects.insert(stocks)

    def find_latest_by_stock(self, stock: str):
        return DailyStockSummary.objects(stock=stock).order_by('-date').first()
