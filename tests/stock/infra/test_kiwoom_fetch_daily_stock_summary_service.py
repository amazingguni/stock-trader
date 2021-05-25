from datetime import date, timedelta
from unittest import mock
import pytest


from core.external.kiwoom import RequestResponse
from core.summary.infra.kiwoom.service import KiwoomFetchDailyStockSummaryService


@pytest.mark.kiwoom
def test_fetch_all(openapi_client):
    summaries = KiwoomFetchDailyStockSummaryService(openapi_client).fetch_all(
        stock_name='삼성전자', stock_code='005930',
        start_date=date(2021, 4, 12), end_date=date(2021, 4, 16))
    assert len(summaries) == 4


def test_mock_fetch_all():
    mock_client = mock.MagicMock()
    mock_client.comm_rq_data_repeat.return_value = RequestResponse(
        has_next=False, error=False, rows=generate_dummy_rows(100)
    )

    summaries = KiwoomFetchDailyStockSummaryService(mock_client).fetch_all(
        stock_name='삼성전자', stock_code='000000',
        start_date=date(2010, 1, 1), end_date=date(2010, 5, 1))

    assert len(summaries) == 100
    assert summaries[0].open == 80
    assert summaries[0].high == 100
    assert summaries[0].low == 70
    assert summaries[0].close == 90
    assert summaries[0].volume == 1000000


def generate_dummy_rows(n):
    current_date = date(2010, 1, 1)
    rows = []
    for _ in range(n):
        rows.append({
            '일자': current_date.strftime('%Y%m%d'),
            '시가': 80,
            '고가': 100,
            '저가': 70,
            '현재가': 90,
            '거래량': 1000000,
        })
        current_date += timedelta(days=1)
    return rows
