from core.account.domain.service import FetchAccountService, FetchAccountDepositService
from core.account.domain.repository import AccountRepository, DepositRepository
from core.common.exception import StockTraderError


class SyncAccountService:
    def __init__(self,
                 account_repository: AccountRepository,
                 deposit_repository: DepositRepository,
                 fetch_account_service: FetchAccountService,
                 fetch_account_deposit_service: FetchAccountDepositService):
        self.account_repository = account_repository
        self.deposit_repository = deposit_repository
        self.fetch_account_service = fetch_account_service
        self.fetch_account_deposit_service = fetch_account_deposit_service

    def sync(self):
        primary_account = self.account_repository.find_primary_account()
        if not (accounts := self.fetch_account_service.fetch_all()):
            raise AccountFetchError()
        for account in accounts:
            if self.account_repository.find_by_account_number(account.number):
                continue
            self.account_repository.save(account)
        primary_account = self.account_repository.find_primary_account(
            {'real': accounts[0].real, 'securities_company': accounts[0].securities_company})
        if not primary_account:
            accounts[0].primary = True
            self.account_repository.save(accounts[0])
            primary_account = accounts[0]
        deposit = self.fetch_account_deposit_service.fetch(
            primary_account.number)
        deposit.account = primary_account
        self.deposit_repository.save(deposit)


class AccountFetchError(StockTraderError):
    pass
