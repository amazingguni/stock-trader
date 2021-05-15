import pytest
from datetime import date

from core.stock.infra.kiwoom.connector import KiwoomConnector

pytestmark = pytest.mark.kiwoom


@pytest.fixture(scope='module')
def connector(application):
    return KiwoomConnector()


def test_get_account_numbers(connector):
    accounts = connector.get_account_numbers()
    assert len(accounts) > 0


def test_get_daily_stock_summaries(connector):
    stocks = connector.get_daily_stock(
        '005930', date(2021, 4, 12), date(2021, 4, 16))
    assert len(stocks) == 4
