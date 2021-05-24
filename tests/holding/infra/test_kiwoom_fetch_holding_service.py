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

# def test_mock_fetch_stocks():
