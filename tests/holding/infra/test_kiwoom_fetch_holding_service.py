from unittest import mock
import pytest

from core.external.kiwoom import RequestResponse
from core.holding.infra.kiwoom.service import KiwoomFetchHoldingService


@pytest.mark.kiwoom
def test_fetch_summary(openapi_client, kiwoom_account):
    # When
    holding_summary = KiwoomFetchHoldingService(
        openapi_client).fetch_summary(kiwoom_account.number)

    # When
    assert holding_summary


@pytest.mark.kiwoom
def test_fetch_stocks(openapi_client, kiwoom_account):
    # When
    KiwoomFetchHoldingService(
        openapi_client).fetch_stocks(kiwoom_account.number)


def test_mock_fetch_summary():
    mock_client = mock.MagicMock()
    mock_client.comm_rq_single_data.return_value = RequestResponse(
        rows=[{
            '총매입금액': 10000, '총평가금액': 9000, '총평가손익금액': 1000,
            '총수익률(%)': 91.1, '추정예탁자산': 10001}])
    holding_summary = KiwoomFetchHoldingService(
        mock_client).fetch_summary('11111111')

    assert holding_summary
    assert holding_summary.total_purchase_price == 10000
    assert holding_summary.total_eval_price == 9000
    assert holding_summary.total_eval_profit_loss_price == 1000

    assert pytest.approx(91.1, 1e-9) == holding_summary.total_earning_rate
    assert holding_summary.estimated_deposit == 10001


def test_mock_fetch_stocks():
    mock_client = mock.MagicMock()
    mock_client.comm_rq_data_repeat.return_value = RequestResponse(
        rows=[{
            '종목번호': "111111",
            '종목명': "삼성전자",
            '보유수량': 10,
            '매입가': 10000,
            '현재가': 9000,
            '평가손익': -1000,
            '수익률(%)': -10,
            '매입금액': 100000,
        }, {
            '종목번호': "222222",
            '종목명': "우리은행",
            '보유수량': 3,
            '매입가': 10,
            '현재가': 11,
            '평가손익': 1,
            '수익률(%)': 10.1,
            '매입금액': 30,
        }])
    holdings = KiwoomFetchHoldingService(
        mock_client).fetch_stocks('11111111')

    assert len(holdings) == 2
    assert holdings[0].stock_code == '111111'
    assert holdings[0].stock_name == '삼성전자'
    assert holdings[0].account_number == '11111111'
    assert holdings[0].quantity == 10

    assert holdings[1].purchase_price == 10
    assert holdings[1].current_price == 11
    assert holdings[1].eval_profit_loss_price == 1
    assert holdings[1].earning_rate == pytest.approx(10.1, 1e-9)
    assert holdings[1].total_purchase_price == 30
