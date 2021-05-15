import time
import typing

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QEventLoop

try:
    from PyQt5.QAxContainer import QAxWidget
except ModuleNotFoundError:
    print("It is only support window environment")
    QAxWidget = object


from .input_value import InputValue
from .response import ConnectResponse, RequestResponse
from .account_info_type import AccountInfoType
from .request_done_condition import RequestDoneCondition, DefaultDoneCondition

TR_REQ_TIME_INTERVAL = 0.2
DEFAULT_SCREEN_NO = '0101'  # It is just random value
FIRST_REQUEST = 0
EXISTING_REQUEST = 2


def sleep_to_wait_transaction():
    time.sleep(TR_REQ_TIME_INTERVAL)


class OpenApiClient(QAxWidget):

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

    def get_login_info(self, info_type: AccountInfoType):
        return self.dynamicCall('GetLoginInfo(QString)', info_type.name)

    def set_input_value(self, _id: str, value: str):
        self.dynamicCall("SetInputValue(QString, QString)", _id, value)

    def comm_rq_data_repeat(self, trcode: str, input_values: typing.List[InputValue],
                            item_key_pair: typing.Dict[str, str], retry: int = 5,
                            done_condition: RequestDoneCondition = DefaultDoneCondition()):
        rqname = f'{trcode}_req'
        response = RequestResponse()
        _next = FIRST_REQUEST
        for _ in range(retry):
            each_response = self.comm_rq_data(
                trcode, rqname, input_values, _next, item_key_pair, done_condition)
            response.rows += each_response.rows
            response.has_next = each_response.has_next
            if not each_response.has_next:
                break
            _next = EXISTING_REQUEST
        return response

    def comm_rq_data(self, trcode: str, rqname: str, input_values: typing.List[InputValue],
                     next: int, item_key_pair: typing.Dict[str, str],
                     done_condition: RequestDoneCondition = DefaultDoneCondition()):
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
                            trcode, rqname, i, item_name)
                    if done_condition.done(row):
                        response.has_next = False
                        break
                    response.rows.append(row)
            finally:
                event_loop.exit()
        self.OnReceiveTrData.connect(receive_tr_data_handler)
        event_loop.exec_()
        return response

    def get_repeat_cnt(self, trcode: str, rqname: str):
        return self.dynamicCall(
            "GetRepeatCnt(QString, QString)", trcode, rqname)

    def get_comm_data(self, code: str, field_name: str, index: int, item_name: str):
        return self.dynamicCall(
            "GetCommData(QString, QString, int, QString)", code, field_name, index, item_name).strip()


class ConnectFailedError(Exception):
    pass
