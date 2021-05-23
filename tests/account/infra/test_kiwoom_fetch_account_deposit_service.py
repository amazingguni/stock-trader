from unittest import mock

from core.account.domain import Account
from core.account.infra.kiwoom.service import KiwoomFetchAccountDepositService
from core.external.kiwoom import RequestResponse


def test_mock_fetch():
    mock_client = mock.MagicMock()
    mock_client.comm_rq_single_data.return_value = RequestResponse(
        rows=[{'예수금': 1000000, 'd+2출금가능금액': 2000000}])
    account = Account(number='12345678')

    ret_deposit = KiwoomFetchAccountDepositService(mock_client).fetch(account)

    assert ret_deposit
    assert ret_deposit.deposit == 1000000
    assert ret_deposit.d2_withdrawable_deposit == 2000000


def test_mock_fetch_GIVEN_failed_THEN_return_None():
    mock_client = mock.MagicMock()
    mock_client.comm_rq_single_data.return_value = RequestResponse(rows=[])
    account = Account(number='12345678')

    ret_deposit = KiwoomFetchAccountDepositService(mock_client).fetch(account)

    assert not ret_deposit
