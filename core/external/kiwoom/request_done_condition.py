import abc
import typing


class RequestDoneCondition:
    @abc.abstractmethod
    def done(self, row: typing.Dict[str, str]):
        raise NotImplementedError


class DefaultDoneCondition(RequestDoneCondition):
    def done(self, row: typing.Dict[str, str]):
        return False
