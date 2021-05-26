from unittest import mock
import pytest

from core.external.kiwoom import RequestResponse
from core.holding.infra.kiwoom.service import KiwoomFetchHoldingSummaryService


@pytest.mark.kiwoom
def test_fetch_summary(openapi_client, kiwoom_account):
    # When
    holding_summary = KiwoomFetchHoldingSummaryService(
        openapi_client).fetch(kiwoom_account.number)

    # When
    assert holding_summary


def client_holdings_response(count):
    rows = []
    for i in range(1, count+1):
        rows.append({
            '종목번호': f'00000{i}',
            '종목명': f"회사_{i}",
            '보유수량': 10,
            '매입가': 10000,
            '현재가': 9000,
            '평가손익': -1000,
            '수익률(%)': -10.1,
            '매입금액': 100000,
        })
    return RequestResponse(rows=rows)


def test_mock_fetch():
    mock_client = mock.MagicMock()
    mock_client.comm_rq_single_data.return_value = RequestResponse(
        rows=[{
            '총매입금액': 10000, '총평가금액': 9000, '총평가손익금액': 1000,
            '총수익률(%)': 91.1, '추정예탁자산': 10001}])
    mock_client.comm_rq_data_repeat.return_value = client_holdings_response(
        count=3)
    holding_summary = KiwoomFetchHoldingSummaryService(
        mock_client).fetch('11111111')

    assert holding_summary
    assert holding_summary.total_purchase_price == 10000
    assert holding_summary.total_eval_price == 9000
    assert holding_summary.total_eval_profit_loss_price == 1000

    assert pytest.approx(91.1, 1e-9) == holding_summary.total_earning_rate
    assert holding_summary.estimated_deposit == 10001

    holdings = holding_summary.holdings
    assert len(holdings) == 3
    assert holdings[0].stock_code == '000001'
    assert holdings[0].stock_name == '회사_1'
    assert holdings[0].quantity == 10
    assert holdings[0].purchase_price == 10000
    assert holdings[0].current_price == 9000
    assert holdings[0].eval_profit_loss_price == -1000
    assert holdings[0].earning_rate == pytest.approx(-10.1, 1e-9)
    assert holdings[0].total_purchase_price == 100000
