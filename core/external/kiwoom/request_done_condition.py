import abc


class RequestDoneCondition:
    @abc.abstractmethod
    def done(self, row: dict[str, str]):
        raise NotImplementedError


class DefaultDoneCondition(RequestDoneCondition):
    def done(self, row: dict[str, str]):
        return False
