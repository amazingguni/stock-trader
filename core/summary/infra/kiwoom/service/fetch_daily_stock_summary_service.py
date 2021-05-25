from time import sleep
from datetime import date, datetime

from core.summary.domain import DailyStockSummary
from core.summary.domain.service import FetchDailyStockSummaryService

from core.external.kiwoom import OpenApiClient, InputValue, RequestDoneCondition, TransactionFailedError


class DailyStockDoneCondition(RequestDoneCondition):
    def __init__(self, start_date: date):
        self.start_date_str = start_date.strftime(
            '%Y%m%d') if start_date else '00000101'

    def done(self, row: dict[str, str]):
        return row['일자'] <= self.start_date_str


class KiwoomFetchDailyStockSummaryService(FetchDailyStockSummaryService):
    def __init__(self, openapi_client: OpenApiClient):
        self.openapi_client = openapi_client

    def fetch_all(self, stock_name: str, stock_code: str, start_date: date, end_date: date):
        input_values = [
            InputValue(s_id='종목코드', s_value=stock_code),
            InputValue(s_id='기준일자', s_value=end_date.strftime('%Y%m%d')),
            InputValue(s_id='수정주가구분', s_value=1),
        ]
        row_keys = ['일자', '시가', '고가', '저가', '현재가', '거래량', ]
        trcode = 'opt10081'
        done_condition = DailyStockDoneCondition(start_date=start_date)
        try:
            response = self.openapi_client.comm_rq_data_repeat(
                trcode, input_values, row_keys,
                done_condition=done_condition)
            return self.rows_to_summaries(response.rows, stock_name, stock_code)
        except TransactionFailedError:
            print(f'Fail to get {stock_code} daily summary. Exit!!')
            sleep(120)
            exit(1)

    def rows_to_summaries(self, rows, stock_name, stock_code):
        summaries = []
        for row in rows:
            summaries.append(DailyStockSummary(
                date=datetime.strptime(row['일자'], '%Y%m%d').date(),
                stock_name=stock_name,
                stock_code=stock_code,
                open=row['시가'],
                high=row['고가'],
                low=row['저가'],
                close=row['현재가'],
                volume=row['거래량']))
        return summaries
