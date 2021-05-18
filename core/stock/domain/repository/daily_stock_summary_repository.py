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

    def find_latest_date_by_stock(self, stock: Stock):
        pipeline = [{
            "$group": {
                '_id':  '$stock',
                'latest_date': {'$max': '$date'}
            }
        }]
        data = list(DailyStockSummary.objects(stock=stock).aggregate(pipeline))
        return data[0]['latest_date'].date() if data else None
