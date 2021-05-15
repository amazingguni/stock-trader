from core.stock.domain.repository.stock_repository import StockRepository


class SyncStockService:
    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository

    def crawl(self):
        kospi_stocks = KospiCollector().collect()
        kosdaq_stocks = KosdaqCollector().collect()
