from unittest import mock

import pytest

from core.account.application import SyncAccountService
from core.account.domain import Account, Deposit


@pytest.mark.kiwoom
def test_sync(account_repository, deposit_repository, fetch_account_service, fetch_account_deposit_service):
    service = SyncAccountService(
        account_repository, deposit_repository,
        fetch_account_service, fetch_account_deposit_service)
    service.sync()

    assert Account.objects.count() > 0
    assert Deposit.objects.count() > 0


def test_mock_sync_GIVEN_no_primary_accounts(account_repository, deposit_repository):
    mock_fetch_account_service = mock.MagicMock()
    account = Account(number='00000000')
    mock_fetch_account_service.fetch_all.return_value = [account]
    mock_fetch_account_deposit_service = mock.MagicMock()
    mock_fetch_account_deposit_service.fetch.return_value = \
        Deposit(deposit=1000000, d2_withdrawable_deposit=2000000)

    service = SyncAccountService(
        account_repository, deposit_repository,
        mock_fetch_account_service, mock_fetch_account_deposit_service)
    service.sync()

    mock_fetch_account_deposit_service.fetch.assert_called_with(account.number)
    assert Account.objects.count() == 1
    assert Account.objects.first().number == '00000000'
    assert Deposit.objects.count() == 1
    deposit = Deposit.objects.first()
    assert deposit.deposit == 1000000
    assert deposit.d2_withdrawable_deposit == 2000000


def test_mock_sync_GIVEN_has_primary_accounts(account_repository, deposit_repository):
    mock_fetch_account_service = mock.MagicMock()
    account = Account(number='00000000')
    mock_fetch_account_service.fetch_all.return_value = [account]
    mock_fetch_account_deposit_service = mock.MagicMock()
    mock_fetch_account_deposit_service.fetch.return_value = \
        Deposit(deposit=1000000, d2_withdrawable_deposit=2000000)
    existing_primary_account = Account(number='99999999', primary=True).save()

    service = SyncAccountService(
        account_repository, deposit_repository,
        mock_fetch_account_service, mock_fetch_account_deposit_service)
    service.sync()

    mock_fetch_account_deposit_service.fetch.assert_called_with(
        existing_primary_account.number)
    assert Account.objects.count() == 2
    assert Deposit.objects.count() == 1


def test_mock_sync_GIVEN_has_real_primary_account_but_connected_imitation_account_THEN_use_imitation_account_as_primary(
        account_repository, deposit_repository):
    mock_fetch_account_service = mock.MagicMock()
    account = Account(number='00000000', real=False)
    mock_fetch_account_service.fetch_all.return_value = [account]
    mock_fetch_account_deposit_service = mock.MagicMock()
    mock_fetch_account_deposit_service.fetch.return_value = \
        Deposit(deposit=1000000, d2_withdrawable_deposit=2000000)
    Account(number='99999999', primary=True, real=True).save()

    service = SyncAccountService(
        account_repository, deposit_repository,
        mock_fetch_account_service, mock_fetch_account_deposit_service)
    service.sync()

    mock_fetch_account_deposit_service.fetch.assert_called_with(
        account.number)


def test_mock_sync_GIVEN_multiple_call_THEN_same_account_only_increase_result(account_repository, deposit_repository):
    mock_fetch_account_service = mock.MagicMock()

    mock_fetch_account_service.fetch_all.side_effect = [
        [Account(number='00000000')],
        [Account(number='00000000')],
        [Account(number='00000000')]
    ]
    mock_fetch_account_deposit_service = mock.MagicMock()
    mock_fetch_account_deposit_service.fetch.side_effect = [
        Deposit(deposit=1000000, d2_withdrawable_deposit=2000000),
        Deposit(deposit=1000000, d2_withdrawable_deposit=2000000),
        Deposit(deposit=1000000, d2_withdrawable_deposit=2000000),
    ]
    Account(number='99999999', primary=True).save()

    service = SyncAccountService(
        account_repository, deposit_repository,
        mock_fetch_account_service, mock_fetch_account_deposit_service)
    service.sync()
    service.sync()
    service.sync()

    assert Account.objects.count() == 2
    assert Deposit.objects.count() == 3
