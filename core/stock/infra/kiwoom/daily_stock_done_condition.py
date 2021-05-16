import typing
from datetime import date

from core.stock.infra.kiwoom.openapi.request_done_condition import RequestDoneCondition


class DailyStockDoneCondition(RequestDoneCondition):
    def __init__(self, start_date: date):
        self.start_date_str = start_date.strftime(
            '%Y%m%d') if start_date else '00000101'

    def done(self, row: typing.Dict[str, str]):
        return row['date'] <= self.start_date_str
