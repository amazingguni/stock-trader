from core.stock.domain.repository.stock_repository import StockRepository
from core.stock.infra.kind.kospi_crawler import KospiCrawler
from core.stock.infra.kind.kosdaq_crawler import KosdaqCrawler
from core.stock.infra.kind.insincerity_crawler import InsincerityCrawler
from core.stock.infra.kind.managing_crawler import ManagingCrawler


class SyncStockService:
    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository

    def sync(self):
        crawled_stocks = []
        for crawler in [KospiCrawler(), KosdaqCrawler()]:
            crawled_stocks += crawler.crawl()
        managing_stocks = ManagingCrawler().crawl()
        insincerity_stocks = InsincerityCrawler().crawl()

        managing_stock_codes = set(
            map(lambda stock: stock.code, managing_stocks))
        insincerity_stock_codes = set(
            map(lambda stock: stock.code, insincerity_stocks))
        self.stock_repository.update_all(query={}, update={'active': False})
        existing_code_stock_dic = {
            stock.code: stock for stock in self.stock_repository.find_all()}
        for stock in crawled_stocks:
            stock.is_managing = stock.code in managing_stock_codes
            stock.is_insincerity = stock.code in insincerity_stock_codes
            stock.active = True
            if existing_stock := existing_code_stock_dic.get(stock.code, None):
                self.stock_repository.update(existing_stock, stock.to_mongo())
                continue
            self.stock_repository.save(stock)
