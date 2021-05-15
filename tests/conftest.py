import pytest
from mongoengine import connect, disconnect, get_connection

from core.stock.domain.repository.stock_repository import StockRepository
from core.stock.domain.repository.daily_stock_summary_repository import DailyStockSummaryRepository


@pytest.fixture(scope='function')
def mongo_connection():
    connect('mongoenginetest', host='mongomock://localhost')
    yield get_connection()
    disconnect()


@pytest.fixture(scope='function')
def stock_repository(mongo_connection):
    return StockRepository()


@pytest.fixture(scope='function')
def daily_stock_summary_repository(mongo_connection):
    return DailyStockSummaryRepository()
