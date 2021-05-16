import pandas as pd

from core.stock.domain.stock_crawler import StockCrawler
from core.stock.domain.stock import MARKET_KOSDAQ
from .helpers import mapper

KOSDAQ_STOCK_LIST = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=kosdaqMkt'


class KosdaqCrawler(StockCrawler):
    def crawl(self):
        df = pd.read_html(KOSDAQ_STOCK_LIST)[0]
        df = df.fillna({'회사명': '', '업종': '', '주요제품': '', '결산월': '', '지역': ''})
        stocks = []
        for _, row in df.iterrows():
            stock = mapper(row)
            stock.market = MARKET_KOSDAQ
            stocks.append(stock)
        return stocks
