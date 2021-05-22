import abc
from core.account.domain import Account


class FetchAccountDepositService:
    @abc.abstractmethod
    def fetch(self, account: Account):
        raise NotImplementedError
