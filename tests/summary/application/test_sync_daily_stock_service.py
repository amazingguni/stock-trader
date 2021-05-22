from datetime import date
from unittest import mock
import pytest

from core.stock.domain import Stock
from core.stock.domain.repository import StockRepository

from core.summary.application import SyncDailyStockSummaryService
from core.summary.domain import DailyStockSummary
from core.summary.domain.repository import DailyStockSummaryRepository


@pytest.fixture(scope='function')
def daily_stock_summary_repository(mongo_connection):
    return DailyStockSummaryRepository()


@pytest.fixture(scope='function')
def stock_repository(mongo_connection):
    return StockRepository()


@pytest.fixture
def stock(mongo_connection):
    stock = Stock(
        name='삼성전자', code='000001', market=Stock.MARKET_KOSDAQ
    )
    stock.save()
    return stock


def get_dummy_daily_stock_summary(stock):
    return DailyStockSummary(
        date=date(2010, 10, 2),
        stock=stock,
        open=1,
        high=1,
        low=1,
        close=1,
        volume=1,
    )


def test_sync(stock_repository, daily_stock_summary_repository, stock):
    mock_fetch_daily_stock_summary_service = mock.MagicMock()
    mock_fetch_daily_stock_summary_service.fetch_all.return_value = \
        [get_dummy_daily_stock_summary(stock)] * 10

    # When
    service = SyncDailyStockSummaryService(
        mock_fetch_daily_stock_summary_service,
        stock_repository, daily_stock_summary_repository)
    service.sync(stock, date(2010, 10, 1), date(2010, 10, 3))

    # Then
    assert DailyStockSummary.objects.count() == 10


def test_sync_all(stock_repository, daily_stock_summary_repository, stock):
    mock_fetch_daily_stock_summary_service = mock.MagicMock()
    mock_fetch_daily_stock_summary_service.fetch_all.return_value = \
        [get_dummy_daily_stock_summary(stock)] * 10

    # When
    service = SyncDailyStockSummaryService(
        mock_fetch_daily_stock_summary_service,
        stock_repository, daily_stock_summary_repository)
    list(service.sync_all())

    # Then
    assert DailyStockSummary.objects.count() == 10
