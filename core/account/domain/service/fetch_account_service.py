import abc


class FetchAccountService:
    @abc.abstractmethod
    def fetch_all(self):
        raise NotImplementedError
