import typing

from core.stock.domain.repository.stock_repository import StockRepository
from core.stock.infra.kind.kospi_crawler import KospiCrawler
from core.stock.infra.kind.kosdaq_crawler import KosdaqCrawler
from core.stock.infra.kind.insincerity_crawler import InsincerityCrawler
from core.stock.infra.kind.managing_crawler import ManagingCrawler


class SyncStockService:
    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository

    def sync(self):
        stocks = []
        for crawler in [KospiCrawler(), KosdaqCrawler()]:
            stocks += crawler.crawl()
        managing_stocks = ManagingCrawler().crawl()
        insincerity_stocks = InsincerityCrawler().crawl()

        managing_stock_codes = set(
            map(lambda stock: stock.code, managing_stocks))
        insincerity_stock_codes = set(
            map(lambda stock: stock.code, insincerity_stocks))
        self.stock_repository.update(update={'active': False})
        for stock in stocks:
            if stock.code in managing_stock_codes:
                stock.is_managing = True
            if stock.code in insincerity_stock_codes:
                stock.is_insincerity = True
            self.stock_repository.save_or_modify(stock)
