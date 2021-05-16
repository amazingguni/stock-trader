import typing
from core.stock.domain.repository.stock_repository import StockRepository
from core.stock.domain.stock_crawler import StockCrawler


class SyncStockService:
    def __init__(self, stock_repository: StockRepository,
                 stock_crawlers: typing.List[StockCrawler]):
        self.stock_repository = stock_repository
        self.stock_crawlers = stock_crawlers

    def sync(self):
        stocks = []
        for crawler in self.stock_crawlers:
            stocks += crawler.crawl()
        for stock in stocks:
            self.stock_repository.save_or_modify(stock)
