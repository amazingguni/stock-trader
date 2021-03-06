import pytest

from core.stock.application.sync_stock_service import SyncStockService

from core.stock.domain.stock import Stock

pytestmark = [pytest.mark.slow]


def test_sync(stock_repository):
    service = SyncStockService(stock_repository=stock_repository)

    service.sync()

    assert Stock.objects.count() > 0


def test_sync_GIVEN_crawl_same_THEN_no_more_stock_saved(stock_repository):
    service = SyncStockService(stock_repository=stock_repository)
    service.sync()
    kosdaq_stocks_cnt = Stock.objects.count()

    # When
    service.sync()

    # Then
    assert Stock.objects.count() == kosdaq_stocks_cnt
