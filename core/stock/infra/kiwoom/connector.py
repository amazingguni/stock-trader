from datetime import date
from time import sleep
from core.stock.domain.stock_connector import StockConnector
from core.stock.infra.kiwoom.openapi.client import OpenApiClient, TransactionFailedError
from core.stock.infra.kiwoom.openapi.account_info_type import AccountInfoType
from core.stock.infra.kiwoom.openapi.input_value import InputValue


from core.stock.domain.stock_summary import DailyStockSummary
from core.stock.domain.stock import Stock

from .daily_stock_done_condition import DailyStockDoneCondition


def parse_date_str(s: str):
    return date(year=int(s[:4]), month=int(s[4:6]), day=int(s[6:]))


class KiwoomConnector(StockConnector):
    def __init__(self, q_application=None):
        self.q_application = q_application
        self.client = OpenApiClient()
        self.client.connect()

    def get_account_numbers(self):
        ret = self.client.get_login_info(AccountInfoType.ACCLIST)
        return list(filter(lambda x: x, ret.split(';')))

    def get_daily_stock_summary(self, stock: Stock, start_date: date, end_date: date):
        input_values = [
            InputValue(s_id='종목코드', s_value=stock.code),
            InputValue(s_id='기준일자', s_value=end_date.strftime('%Y%m%d')),
            InputValue(s_id='수정주가구분', s_value=1),
        ]
        item_key_pair = {
            '일자': 'date',
            '시가': 'open',
            '고가': 'high',
            '저가': 'low',
            '현재가': 'close',
            '거래량': 'volume',
        }
        trcode = 'opt10081'
        done_condition = DailyStockDoneCondition(start_date=start_date)

        def mapper(row):
            _date = parse_date_str(row['date'])
            del row['date']
            return DailyStockSummary(date=_date, stock=stock, **row)
        for i in range(1, 21):
            try:
                response = self.client.comm_rq_data_repeat(
                    trcode, input_values, item_key_pair,
                    done_condition=done_condition)
                return [mapper(row) for row in response.rows], response.has_next
            except TransactionFailedError:
                print(f'Fail to get {stock.name} daily summary. Retry')
                sleep(60 * i)
