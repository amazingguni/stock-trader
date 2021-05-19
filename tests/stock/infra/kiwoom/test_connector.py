from datetime import date

import pytest

from core.stock.infra.kiwoom.connector import KiwoomConnector
from core.stock.domain.stock import Stock

pytestmark = [pytest.mark.kiwoom, pytest.mark.slow]


@pytest.fixture(scope='package')
def connector(client):
    return KiwoomConnector(client)


def test_get_account_numbers(connector):
    accounts = connector.get_account_numbers()
    assert len(accounts) > 0


def test_get_daily_stock_summary(connector):
    stock = Stock(
        name='회사',
        code='005930'
    )
    stocks, _ = connector.get_daily_stock_summary(
        stock, date(2021, 4, 12), date(2021, 4, 16))
    assert len(stocks) == 4


def test_get_account_deposit(connector):
    deposit = connector.get_account_deposit()
    assert deposit.deposit > 0
    assert deposit.d2_withdrawable_deposit > 0
