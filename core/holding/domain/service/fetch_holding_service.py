import abc


class FetchHoldingService:
    @abc.abstractmethod
    def fetch_stocks(self, account_number: str):
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_summary(self, account_number: str):
        raise NotImplementedError
