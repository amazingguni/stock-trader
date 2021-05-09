import typing
from core.stock.domain.stock import DailyStock


class DailyStockRepository:
    def __init__(self):
        pass

    def save(self, stock: DailyStock):
        stock.save()

    def save_all(self, stocks: typing.List[DailyStock]):
        DailyStock.objects.insert(stocks)

    def find_latest_by_stock_code(self, stock_code: str):
        return DailyStock.objects(stock_code=stock_code).order_by('-date').first()
