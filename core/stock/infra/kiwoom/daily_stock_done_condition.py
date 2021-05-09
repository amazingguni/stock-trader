import typing
from datetime import date

from core.stock.infra.kiwoom.openapi.request_done_condition import RequestDoneCondition


class DailyStockDoneCondition(RequestDoneCondition):
    def __init__(self, start_date: date):
        self.start_date_str = start_date.strftime('%Y%m%d')

    def done(self, row: typing.Dict[str, str]):
        return row['date'] <= self.start_date_str
