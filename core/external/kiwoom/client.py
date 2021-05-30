from core.external.kiwoom.chejan_type import ChejanType
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
from .bidding_type import BiddingType
from .order_type import OrderType
from .order_concluded_handler import OrderConcludedHandler, OrderConcludedEvent, ConclusionType

DYNAMIC_TIME_INTERVAL = 0.2
TR_REQ_TIME_INTERVAL = 3.6

DEFAULT_SCREEN_NO = '0101'  # It is just random value

FIRST_REQUEST = 0
EXISTING_REQUEST = 2

CHEJAN_CONCLUSION = '0'

def sleep_to_wait_dynamic_call():
    time.sleep(DYNAMIC_TIME_INTERVAL)


def sleep_to_wait_transaction():
    time.sleep(TR_REQ_TIME_INTERVAL)


class OpenApiClient(QAxWidget):
    def __init__(self):
        super().__init__()
        self.__create_open_api_instance()
        self.OnReceiveMsg.connect(self.__receive_msg)
        self.OnReceiveChejanData.connect(self.__receive_chejan_data)
        self.order_concluded_handler = None

    def __create_open_api_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def __receive_msg(self, sScrNo, sRQName, sTrCode, sMsg):
        print(sMsg)
    
    def __receive_chejan_data(self, gubun, item_cnt, fid_list):
        if gubun == CHEJAN_CONCLUSION:
            # pass
            self.__receive_conclusion_data()
        
    def __receive_conclusion_data(self):
        order_type = self.get_chejan_data(ChejanType.ORDER_TYPE)
        conclusion_type = ConclusionType.BID if order_type == '+매수' else ConclusionType.ASK
        conclusion_number = self.get_chejan_data(ChejanType.CONCLUSION_NUMBER)
        stock_code = self.get_chejan_data(ChejanType.STOCK_CODE)
        account_number = self.get_chejan_data(ChejanType.ACCOUNT_NUMBER)
        
        concluded_price = self.get_chejan_data(ChejanType.CONCLUDED_PRICE)
        
        ordered_quantity = self.get_chejan_data(ChejanType.ORDERED_QUANTITY)
        concluded_quantity = self.get_chejan_data(ChejanType.CONCLUDED_QUANTITY)
        balanced_quantity = self.get_chejan_data(ChejanType.BALANCED_QUANTITY)

        concluded_at = self.get_chejan_data(ChejanType.CONCLUDED_AT)

        event = OrderConcludedEvent(
            conclusion_type=conclusion_type,
            conclusion_number=conclusion_number,
            stock_code=stock_code,
            account_number=account_number,
            concluded_price=concluded_price,
            ordered_quantity=ordered_quantity,
            concluded_quantity=concluded_quantity,
            balanced_quantity=balanced_quantity,
            concluded_at=concluded_at
        )
        if self.order_concluded_handler:
            self.order_concluded_handler.handle(event)


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

    def dynamic_call(self, method, *args, **kwargs):
        ret = self.dynamicCall(method, *args, **kwargs)
        if ret == -200:
            raise RateLimitExceeded()
        if isinstance(ret, int) and ret < 0:
            raise DynamicCallFailedError()
        return ret
    
    def get_connect_state(self):
        return self.dynamic_call('GetConnectState()')

    def get_login_info(self, info_type: AccountInfoType):
        return self.dynamic_call('GetLoginInfo(QString)', info_type.name)

    def set_input_value(self, _id: str, value: str):
        self.dynamic_call("SetInputValue(QString, QString)", _id, value)

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
        self.dynamic_call(
            "CommRqData(QString, QString, int, QString)", rqname, trcode, next, DEFAULT_SCREEN_NO)

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
        self.dynamic_call(
            "CommRqData(QString, QString, int, QString)", rqname, trcode, FIRST_REQUEST, DEFAULT_SCREEN_NO)
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
        return self.dynamic_call(
            "GetRepeatCnt(QString, QString)", trcode, rqname)

    def get_comm_data(self, code: str, field_name: str, index: int, item_name: str):
        return self.dynamic_call(
            "GetCommData(QString, QString, int, QString)", code, field_name, index, item_name).strip()

    def send_order(self, account_number:str, order_type:OrderType, stock_code:str, quantity:int, price:int, bidding_type:BiddingType, origin_order_no:str=''):
        rqname = 'send_order_req'
        return self.dynamic_call("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                             [rqname, DEFAULT_SCREEN_NO, account_number, order_type.value, stock_code, quantity, price, bidding_type.value, origin_order_no])
    
    def register_order_concluded_handler(self, handler:OrderConcludedHandler):
        self.order_concluded_handler = handler
    
    def get_chejan_data(self, fid):
        return self.dynamic_call('GetChejanData(int)', fid)