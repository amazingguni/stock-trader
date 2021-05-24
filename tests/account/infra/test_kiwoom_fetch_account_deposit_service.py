from unittest import mock
import pytest

from core.account.infra.kiwoom.service import KiwoomFetchAccountDepositService
from core.external.kiwoom import RequestResponse


@pytest.mark.kiwoom
def test_fetch(openapi_client, kiwoom_account):
    # When
    deposit = KiwoomFetchAccountDepositService(
        openapi_client).fetch(kiwoom_account.number)

    assert deposit


def test_mock_fetch():
    mock_client = mock.MagicMock()
    mock_client.comm_rq_single_data.return_value = RequestResponse(
        rows=[{'예수금': 1000000, 'd+2출금가능금액': 2000000}])

    ret_deposit = KiwoomFetchAccountDepositService(mock_client).fetch(12345678)

    assert ret_deposit
    assert ret_deposit.deposit == 1000000
    assert ret_deposit.d2_withdrawable_deposit == 2000000


def test_mock_fetch_GIVEN_failed_THEN_return_None():
    mock_client = mock.MagicMock()
    mock_client.comm_rq_single_data.return_value = RequestResponse(rows=[])

    ret_deposit = KiwoomFetchAccountDepositService(
        mock_client).fetch('12345678')

    assert not ret_deposit
