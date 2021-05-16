from datetime import date
from unittest import mock
import pytest

from core.stock.application.crawl_daily_stock_summary_service import CrawlDailyStockSummaryService
from core.stock.domain.stock_summary import DailyStockSummary
from core.stock.domain.stock import Stock

from core.stock.domain.repository.daily_stock_summary_repository import DailyStockSummaryRepository
from core.stock.domain.repository.stock_repository import StockRepository


@pytest.fixture(scope='function')
def daily_stock_summary_repository(mongo_connection):
    return DailyStockSummaryRepository()


@pytest.fixture(scope='function')
def stock_repository(mongo_connection):
    return StockRepository()


@pytest.fixture
def stock(mongo_connection):
    stock = Stock(
        name='삼성전자', code='000001'
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


def test_crawl(stock_repository, daily_stock_summary_repository, stock):
    mock_connector = mock.MagicMock()
    mock_connector.get_daily_stock_summary.return_value = [
        get_dummy_daily_stock_summary(stock)] * 10

    # When
    service = CrawlDailyStockSummaryService(
        mock_connector, stock_repository, daily_stock_summary_repository)
    service.crawl(stock)

    # Then
    assert DailyStockSummary.objects.count() == 10


def test_crawl_all(stock_repository, daily_stock_summary_repository, stock):
    mock_connector = mock.MagicMock()
    mock_connector.get_daily_stock_summary.return_value = [
        get_dummy_daily_stock_summary(stock)] * 10

    # When
    service = CrawlDailyStockSummaryService(
        mock_connector, stock_repository, daily_stock_summary_repository)
    service.crawl_all()

    # Then
    assert DailyStockSummary.objects.count() == 10
