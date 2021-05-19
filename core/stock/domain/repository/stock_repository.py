
import typing
from core.stock.domain.stock import Stock


class StockRepository:
    def __init__(self):
        pass

    def save_or_modify(self, stock: Stock):
        if existing_stock := Stock.objects(code=stock.code).first():
            existing_stock.update(**stock.to_mongo())
        else:
            self.save(stock)

    def save(self, stock: Stock):
        stock.save()

    def save_all(self, stocks: typing.List[Stock]):
        Stock.objects.insert(stocks)

    def find_all(self):
        return Stock.objects.all()

    def update_all(self, query={}, update={}):
        Stock.objects(**query).update(**update)

    def update(self, stock, update={}):
        stock.update(**update)
