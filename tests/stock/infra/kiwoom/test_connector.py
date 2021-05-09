import pytest
from core.stock.infra.kiwoom.connector import KiwoomConnector


@pytest.fixture(scope='module')
def connector(application):
    return KiwoomConnector()


def test_get_account_numbers(connector):
    accounts = connector.get_account_numbers()
    assert len(accounts) > 0


def test_get_daily_stock_summaries(connector):
    stocks = connector.get_daily_stock('005930', '20210424')
    assert len(stocks) > 0
