import pytest
from datetime import datetime
from mongoengine import connect, disconnect, get_connection

from core.stock.domain.repository.daily_stock_repository import DailyStockRepository
from core.stock.domain.stock import DailyStock, StockSummary


@pytest.fixture(scope='function')
def connection():
    connect('mongoenginetest', host='mongomock://localhost')
    yield get_connection()
    disconnect()


def test_save(connection):
    stock = DailyStock(
        date=datetime.now(),
        stock_summary=StockSummary(
            open=1,
            high=1,
            low=1,
            close=1,
            volume=1,
        )
    )
    # When
    DailyStockRepository().save(stock)

    assert DailyStock.objects.count() == 1


def test_save_all(connection):
    stock = DailyStock(
        date=datetime.now(),
        stock_summary=StockSummary(
            open=1,
            high=1,
            low=1,
            close=1,
            volume=1,
        )
    )
    stocks = [stock] * 10
    # When
    DailyStockRepository().save_all(stocks)

    # Then
    assert DailyStock.objects.count() == 10
