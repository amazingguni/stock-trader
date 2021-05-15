from datetime import date
from unittest import mock
import pytest

from core.stock.application.crawl_daily_stock_summary_service import CrawlDailyStockSummaryService
from core.stock.domain.stock_summary import DailyStockSummary
from core.stock.domain.repository.daily_stock_summary_repository import DailyStockSummaryRepository


@pytest.fixture(scope='function')
def daily_stock_summary_repository(mongo_connection):
    return DailyStockSummaryRepository()


def get_dummy_daily_stock_summary():
    return DailyStockSummary(
        date=date(2010, 10, 2),
        stock_code='CODE',
        open=1,
        high=1,
        low=1,
        close=1,
        volume=1,
    )


def test_crawl(daily_stock_summary_repository):
    mock_connector = mock.MagicMock()
    mock_connector.get_daily_stock_summary.return_value = [
        get_dummy_daily_stock_summary()] * 10

    # When
    service = CrawlDailyStockSummaryService(
        mock_connector, daily_stock_summary_repository)
    service.crawl('STOCK_CODE')

    # Then
    assert DailyStockSummary.objects.count() == 10
