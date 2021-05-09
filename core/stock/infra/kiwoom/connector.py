import sys

from PyQt5.QtWidgets import QApplication

from core.stock.infra.kiwoom.openapi.client import OpenApiClient
from core.stock.infra.kiwoom.openapi.account_info_type import AccountInfoType
from core.stock.infra.kiwoom.openapi.input_value import InputValue


class KiwoomConnector:
    def __init__(self):
        self.client = OpenApiClient()
        self.client.connect()

    def get_account_numbers(self):
        ret = self.client.get_login_info(AccountInfoType.ACCLIST)
        return list(filter(lambda x: x, ret.split(';')))

    def get_daily_stock(self, stock_code: str, last_date: str):
        input_values = [
            InputValue(s_id='종목코드', s_value=stock_code),
            InputValue(s_id='기준일자', s_value=last_date),
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
        ret = self.client.comm_rq_data_repeat(
            input_values, trcode, item_key_pair)
