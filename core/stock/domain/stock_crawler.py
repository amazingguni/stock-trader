import abc


class StockCrawler(abc.ABC):
    @abc.abstractmethod
    def crawl(self):
        raise NotImplementedError
