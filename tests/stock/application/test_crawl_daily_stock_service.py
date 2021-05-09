import pytest
from datetime import date
from unittest import mock
from core.stock.application.crawl_daily_stock_service import CrawlDailyStockService
from core.stock.domain.stock import DailyStock, StockSummary
from core.stock.domain.repository.daily_stock_repository import DailyStockRepository


@pytest.fixture(scope='function')
def daily_stock_repository(mongo_connection):
    return DailyStockRepository()


def get_dummy_daily_stock():
    return DailyStock(
        date=date(2010, 10, 2),
        stock_code='CODE',
        stock_summary=StockSummary(
            open=1,
            high=1,
            low=1,
            close=1,
            volume=1,
        )
    )


def test_crawl(daily_stock_repository):
    mock_connector = mock.MagicMock()
    mock_connector.get_daily_stock.return_value = [
        get_dummy_daily_stock()] * 10

    # When
    CrawlDailyStockService(mock_connector, daily_stock_repository).crawl(
        'STOCK_CODE', date.today())

    # Then
    assert DailyStock.objects.count() == 10
