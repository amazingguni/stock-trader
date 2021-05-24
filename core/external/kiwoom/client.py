import time
import traceback

from PyQt5.QtCore import QEventLoop, QTimer

try:
    from PyQt5.QAxContainer import QAxWidget
except ModuleNotFoundError:
    print("It is only support window environment")
    QAxWidget = object


from .input_value import InputValue
from .response import ConnectResponse, RequestResponse
from .account_info_type import AccountInfoType
from .request_done_condition import RequestDoneCondition, DefaultDoneCondition
from .exceptions import ConnectFailedError, TransactionFailedError, RateLimitExceeded, DynamicCallFailedError

DYNAMIC_TIME_INTERVAL = 0.2
TR_REQ_TIME_INTERVAL = 3.6

DEFAULT_SCREEN_NO = '0101'  # It is just random value

FIRST_REQUEST = 0
EXISTING_REQUEST = 2


def sleep_to_wait_dynamic_call():
    time.sleep(DYNAMIC_TIME_INTERVAL)


def sleep_to_wait_transaction():
    time.sleep(TR_REQ_TIME_INTERVAL)


class OpenApiClient(QAxWidget):
    def __init__(self):
        super().__init__()
        self.__create_open_api_instance()
        self.OnReceiveMsg.connect(self.__receive_msg)

    def __create_open_api_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def __receive_msg(self, sScrNo, sRQName, sTrCode, sMsg):
        print(sMsg)

    def connect(self):
        response = ConnectResponse()
        login_event_loop = QEventLoop()

        def event_connect_handler(err_code):
            response.error_code = err_code
            login_event_loop.exit()

        self.OnEventConnect.connect(event_connect_handler)
        sleep_to_wait_dynamic_call()
        self.dynamicCall('CommConnect()')
        login_event_loop.exec_()
        self.OnEventConnect.disconnect()
        if response.error_code != 0:
            self.__create_open_api_instance()
            raise ConnectFailedError

    def get_connect_state(self):
        return self.dynamicCall('GetConnectState()')

    def get_login_info(self, info_type: AccountInfoType):
        ret = self.dynamicCall('GetLoginInfo(QString)', info_type.name)
        if ret == None:
            raise DynamicCallFailedError()
        return ret

    def set_input_value(self, _id: str, value: str):
        self.dynamicCall("SetInputValue(QString, QString)", _id, value)

    def comm_rq_data_repeat(self, trcode: str, input_values: list[InputValue],
                            row_keys: list[str], retry: int = 40,
                            done_condition: RequestDoneCondition = DefaultDoneCondition()):
        response = RequestResponse()
        _next = FIRST_REQUEST
        for _ in range(retry):
            each_response = self.comm_rq_data(
                trcode, input_values, _next, row_keys, done_condition)
            response.rows += each_response.rows
            response.has_next = each_response.has_next
            sleep_to_wait_transaction()
            if not each_response.has_next:
                break
            _next = EXISTING_REQUEST

        return response

    def comm_rq_data(self, trcode: str, input_values: list[InputValue],
                     next: int, row_keys: list[str],
                     done_condition: RequestDoneCondition = DefaultDoneCondition()):
        if not self.get_connect_state():
            self.connect()
        rqname = f'{trcode}_req'
        for input_value in input_values:
            self.set_input_value(input_value.s_id, input_value.s_value)
        ret = self.dynamicCall(
            "CommRqData(QString, QString, int, QString)", rqname, trcode, next, DEFAULT_SCREEN_NO)
        if ret == -200:
            raise RateLimitExceeded()

        response = RequestResponse()
        event_loop = QEventLoop()

        def receive_tr_data_handler(screen_no, rqname, trcode, record_name, next,
                                    unused1, unused2, unused3, unused4):
            try:
                response.has_next = next == '2'
                repeat_cnt = self.get_repeat_cnt(trcode, rqname)
                for i in range(repeat_cnt):
                    row = {}
                    for key in row_keys:
                        row[key] = self.get_comm_data(
                            trcode, rqname, i, key)
                    if done_condition.done(row):
                        response.has_next = False
                        break
                    response.rows.append(row)
            except Exception:
                traceback.print_exc()
                response.error = True
            finally:
                if event_loop.isRunning():
                    event_loop.exit()
        self.OnReceiveTrData.connect(receive_tr_data_handler)

        def loop_timeout():
            if event_loop.isRunning():
                print('event_loop looks not working')
                response.error = True
                event_loop.exit()
        QTimer.singleShot(3000, loop_timeout)
        event_loop.exec_()
        self.OnReceiveTrData.disconnect()
        if response.error:
            raise TransactionFailedError
        return response

    def comm_rq_single_data(self, trcode: str, input_values: list[InputValue],
                            row_keys: list[str]):
        if not self.get_connect_state():
            self.connect()
        for input_value in input_values:
            self.set_input_value(input_value.s_id, input_value.s_value)
        rqname = f'{trcode}_req'
        ret = self.dynamicCall(
            "CommRqData(QString, QString, int, QString)", rqname, trcode, FIRST_REQUEST, DEFAULT_SCREEN_NO)
        if ret == -200:
            raise RateLimitExceeded()

        response = RequestResponse()
        event_loop = QEventLoop()

        def receive_tr_data_handler(screen_no, rqname, trcode, record_name, next,
                                    unused1, unused2, unused3, unused4):
            try:
                row = {}
                for key in row_keys:
                    row[key] = self.get_comm_data(trcode, rqname, 0, key)
                response.rows.append(row)
            except Exception:
                traceback.print_exc()
                response.error = True
            finally:
                if event_loop.isRunning():
                    event_loop.exit()
        self.OnReceiveTrData.connect(receive_tr_data_handler)

        def loop_timeout():
            if event_loop.isRunning():
                print('event_loop looks not working')
                response.error = True
                event_loop.exit()
        QTimer.singleShot(3000, loop_timeout)
        event_loop.exec_()
        self.OnReceiveTrData.disconnect(receive_tr_data_handler)
        if response.error:
            raise TransactionFailedError
        return response

    def get_repeat_cnt(self, trcode: str, rqname: str):
        return self.dynamicCall(
            "GetRepeatCnt(QString, QString)", trcode, rqname)

    def get_comm_data(self, code: str, field_name: str, index: int, item_name: str):
        return self.dynamicCall(
            "GetCommData(QString, QString, int, QString)", code, field_name, index, item_name).strip()
