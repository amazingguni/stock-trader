from core.summary.domain import DailyStockSummary


class DailyStockSummaryRepository:
    def __init__(self):
        pass

    def save(self, stock: DailyStockSummary):
        stock.save()

    def save_all(self, stocks: list[DailyStockSummary]):
        if stocks:
            DailyStockSummary.objects.insert(stocks)

    def find_latest_dates_by_stock_id(self):
        pipeline = [{
            "$group": {
                '_id':  '$stock_code',
                'latest_date': {'$max': '$date'}
            }
        }]
        cursor = DailyStockSummary.objects.aggregate(pipeline)
        return {item['_id']: item['latest_date'].date() for item in cursor}

    def delete_by_stock_code(self, stock_code: str):
        DailyStockSummary.objects(stock_code=stock_code).delete()
