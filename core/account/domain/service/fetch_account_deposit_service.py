import abc


class FetchAccountDepositService:
    @abc.abstractmethod
    def fetch(self, account_number: str):
        raise NotImplementedError
