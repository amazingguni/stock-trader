import abc


class FetchHoldingSummaryService:
    @abc.abstractmethod
    def fetch(self, account_number: str):
        raise NotImplementedError
