import time
import sys

from dataclasses import dataclass, field

from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop

TR_REQ_TIME_INTERVAL = 0.2
DEFAULT_SCREEN_NO = '0101'  # It is just random value
FIRST_REQUEST = 0
EXISTING_REQUEST = 2


def sleep_to_wait_transaction():
    time.sleep(TR_REQ_TIME_INTERVAL)


@dataclass
class InputValue:
    s_id: str
    s_value: 'typing.Any'


@dataclass
class ConnectResponse:
    error_code: int = 0


@dataclass
class RequestResponse:
    has_next: bool = False
    rows: list = field(default_factory=list)


class KiwoomOpenApiConnector(QAxWidget):

    def __init__(self):
        super().__init__()
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def connect(self):
        response = ConnectResponse()
        login_event_loop = QEventLoop()

        def event_connect_handler(err_code):
            response.error_code = err_code
            login_event_loop.exit()

        self.OnEventConnect.connect(event_connect_handler)
        self.dynamicCall('CommConnect()')
        sleep_to_wait_transaction()

        login_event_loop.exec_()

        if response.error_code != 0:
            raise ConnectFailedError

    def get_connect_state(self):
        return self.dynamicCall('GetConnectState()')

    def retrieve_accounts(self):
        ret = self.dynamicCall('GetLoginInfo(QString)', 'ACCNO')
        accounts = ret.split(';')
        return accounts

    def set_input_value(self, _id, value):
        self.dynamicCall("SetInputValue(QString, QString)", _id, value)

    def comm_rq_data_repeat(self, input_values, rqname, trcode, item_key_pair, retry=5):
        response = RequestResponse()
        _next = FIRST_REQUEST
        for _ in range(retry):
            each_response = self.comm_rq_data(
                input_values, rqname, trcode, _next, item_key_pair)
            response.rows += each_response.rows
            response.has_next = each_response.has_next
            if each_response.has_next:
                _next = EXISTING_REQUEST
        return response

    def comm_rq_data(self, input_values, rqname, trcode, next, item_key_pair):
        for input_value in input_values:
            self.set_input_value(input_value.s_id, input_value.s_value)
        self.dynamicCall(
            "CommRqData(QString, QString, int, QString)", rqname, trcode, next, DEFAULT_SCREEN_NO)
        sleep_to_wait_transaction()
        response = RequestResponse()
        event_loop = QEventLoop()
        def receive_tr_data_handler(screen_no, rqname, trcode, record_name, next,
                                    unused1, unused2, unused3, unused4):
            try:
                response.has_next = next == '2'
                repeat_cnt = self.get_repeat_cnt(trcode, rqname)
                for i in range(repeat_cnt):
                    row = {}
                    for item_name, key in item_key_pair.items():
                        row[key] = self.get_comm_data(
                            trcode, rqname, i, item_name),
                    response.rows.append(row)
            finally:
                event_loop.exit()
        self.OnReceiveTrData.connect(receive_tr_data_handler)
        event_loop.exec_()
        return response

    def get_repeat_cnt(self, trcode, rqname):
        return self.dynamicCall(
            "GetRepeatCnt(QString, QString)", trcode, rqname)

    def get_comm_data(self, code, field_name, index, item_name):
        return self.dynamicCall(
            "GetCommData(QString, QString, int, QString)", code, field_name, index, item_name).strip()


class ConnectFailedError(Exception):
    pass
