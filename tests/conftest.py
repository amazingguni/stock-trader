import sys
import pytest

from PyQt5.QtWidgets import QApplication

from mongoengine import connect, disconnect, get_connection

from core.stock.domain.repository.stock_repository import StockRepository
from core.summary.domain.repository import DailyStockSummaryRepository

from core.external.kiwoom import OpenApiClient


@pytest.fixture(scope='function')
def mongo_connection():
    disconnect()
    connect('mongoenginetest', host='mongomock://localhost')
    yield get_connection()
    disconnect()


@pytest.fixture(scope='function')
def stock_repository(mongo_connection):
    return StockRepository()


@pytest.fixture(scope='function')
def daily_stock_summary_repository(mongo_connection):
    return DailyStockSummaryRepository()


@pytest.fixture(scope='session')
def openapi_client():
    if not QApplication.instance():
        _ = QApplication(sys.argv)
    client = OpenApiClient()
    client.connect()
    yield client
