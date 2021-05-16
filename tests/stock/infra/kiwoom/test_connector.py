import pytest
from datetime import date

from core.stock.infra.kiwoom.connector import KiwoomConnector
from core.stock.domain.stock import Stock

pytestmark = [pytest.mark.kiwoom, pytest.mark.slow]


@pytest.fixture(scope='module')
def connector(application):
    return KiwoomConnector()


def test_get_account_numbers(connector):
    accounts = connector.get_account_numbers()
    assert len(accounts) > 0


def test_get_daily_stock_summary(connector):
    stock = Stock(
        name='회사',
        code='005930'
    )
    stocks = connector.get_daily_stock_summary(
        stock, date(2021, 4, 12), date(2021, 4, 16))
    assert len(stocks) == 4
