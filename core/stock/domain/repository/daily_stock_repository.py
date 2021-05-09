import typing
from core.stock.domain.stock import DailyStock


class DailyStockRepository:
    def __init__(self):
        pass

    def save(self, stock: DailyStock):
        stock.save()

    def save_all(self, stocks: typing.List[DailyStock]):
        DailyStock.objects.insert(stocks)
