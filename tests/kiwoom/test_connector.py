import sys
import pytest
from PyQt5.QtWidgets import QApplication

from core.kiwoom.connector import KiwoomOpenApiConnector


@pytest.fixture(scope="session")
def application():
    return QApplication(sys.argv)


@pytest.fixture(scope="module")
def connector(application):
    connector = KiwoomOpenApiConnector()
    connector.connect()
    return connector


def test_get_connect_state(connector):
    assert connector.get_connect_state()


def test_retrieve_accounts(connector):
    # When
    accounts = connector.retrieve_accounts()

    # Then
    assert len(accounts) > 0


def test_get_total_data(connector):
    connector.set_input_value("종목코드", '005930')
    connector.set_input_value("기준일자", '20200424')
    connector.set_input_value("수정주가구분", 1)
    rqname = 'opt10081_req'
    trcode = 'opt10081'
    result, has_remain_data = connector.comm_rq_data(rqname, trcode, 0, "0101")
    print(result[0], has_remain_data)

    for _ in range(100):
        connector.set_input_value("종목코드", '005930')
        connector.set_input_value("기준일자", '20200424')
        connector.set_input_value("수정주가구분", 1)
        result, has_remain_data = connector.comm_rq_data(
            rqname, trcode, 2, "0101")
        print(result[0], has_remain_data)
        if not has_remain_data:
            break

    assert 'repeat_cnt' == 'asdf'
