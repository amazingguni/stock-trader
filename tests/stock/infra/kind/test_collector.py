from core.stock.infra.kind.kospi_collector import KospiCollector
from core.stock.infra.kind.kosdaq_collector import KosdaqCollector


def test_kospi_collector():
    stocks = KospiCollector().collect()
    assert len(stocks) > 0


def test_kosdaq_collector():
    stocks = KosdaqCollector().collect()
    assert len(stocks) > 0
