import time
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop

TR_REQ_TIME_INTERVAL = 0.2


def sleep_to_wait_transaction():
    time.sleep(TR_REQ_TIME_INTERVAL)


class KiwoomOpenApiConnector(QAxWidget):
    def __init__(self):
        super().__init__()
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def connect(self):
        error_code = 0
        login_event_loop = QEventLoop()

        def event_connect_handler(err_code):
            error_code = err_code
            login_event_loop.exit()

        self.OnEventConnect.connect(event_connect_handler)
        self.dynamicCall('CommConnect()')
        sleep_to_wait_transaction()

        login_event_loop.exec_()

        if error_code != 0:
            raise ConnectFailedError

    def get_connect_state(self):
        return self.dynamicCall('GetConnectState()')

    def retrieve_accounts(self):
        ret = self.dynamicCall('GetLoginInfo(QString)', 'ACCNO')
        accounts = ret.split(';')
        return accounts

    def set_input_value(self, _id, value):
        self.dynamicCall("SetInputValue(QString, QString)", _id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall(
            "CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        sleep_to_wait_transaction()
        result = []
        self.has_remain = False
        event_loop = QEventLoop()
        def receive_tr_data_handler(screen_no, rqname, trcode, record_name, next,
                                    unused1, unused2, unused3, unused4):
            try:
                self.has_remain = next == '2'
                repeat_cnt = self.get_repeat_cnt(trcode, rqname)
                for i in range(repeat_cnt):
                    result.append({
                        'date': self.get_comm_data(trcode, rqname, i, '일자'),
                        'high': self.get_comm_data(trcode, rqname, i, '고가')
                    })
            finally:
                event_loop.exit()
        self.OnReceiveTrData.connect(receive_tr_data_handler)
        event_loop.exec_()
        return result, self.has_remain

    def get_repeat_cnt(self, trcode, rqname):
        return self.dynamicCall(
            "GetRepeatCnt(QString, QString)", trcode, rqname)

    def get_comm_data(self, code, field_name, index, item_name):
        return self.dynamicCall(
            "GetCommData(QString, QString, int, QString)", code, field_name, index, item_name).strip()


class ConnectFailedError(Exception):
    pass
