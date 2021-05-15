from core.stock.infra.kind.kospi_crawler import KospiCrawler
from core.stock.infra.kind.kosdaq_crawler import KosdaqCrawler


def test_kospi_crawler():
    stocks = KospiCrawler().crawl()
    assert len(stocks) > 0


def test_kosdaq_crawler():
    stocks = KosdaqCrawler().crawl()
    assert len(stocks) > 0
