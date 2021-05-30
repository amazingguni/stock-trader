import typing
import abc
from dataclasses import dataclass
from enum import Enum, auto


class ConclusionType(Enum):
    BID = auto()
    ASK = auto()


@dataclass
class OrderConcludedEvent:
    conclusion_type: ConclusionType
    conclusion_number: int
    stock_code: str
    account_number: str
    concluded_price: int
    ordered_quantity: int
    concluded_quantity: int
    balanced_quantity: int
    concluded_at: typing.Any


class OrderConcludedHandler:
    @abc.abstractmethod
    def handle(self, event: OrderConcludedEvent):
        raise NotImplementedError
