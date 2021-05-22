from unittest import mock
import pytest

from core.account.infra.kiwoom.service import KiwoomFetchAccountService
from core.account.domain import SECURITIES_COMPANY_KIWOOM
from core.external.kiwoom import IMITATION_SERVER


@pytest.mark.kiwoom
def test_fetch_all(openapi_client):
    accounts = KiwoomFetchAccountService(openapi_client).fetch_all()
    assert len(accounts) > 0


def test_mock_fetch_all_GIVEN_IMITATION_SERVER():
    mock_client = mock.MagicMock()
    mock_client.get_login_info.side_effect = [
        IMITATION_SERVER, '12345678;87654321']

    accounts = KiwoomFetchAccountService(mock_client).fetch_all()

    assert len(accounts) == 2
    assert accounts[0].number == '12345678'
    assert accounts[0].securities_company == SECURITIES_COMPANY_KIWOOM
    assert not accounts[0].real


def test_mock_fetch_all_REAL_SERVER():
    mock_client = mock.MagicMock()
    mock_client.get_login_info.side_effect = [
        3, '12345678;87654321']

    accounts = KiwoomFetchAccountService(mock_client).fetch_all()

    assert len(accounts) == 2
    assert accounts[0].number == '12345678'
    assert accounts[0].securities_company == SECURITIES_COMPANY_KIWOOM
    assert accounts[0].real
