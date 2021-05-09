import sys
import pytest
from PyQt5.QtWidgets import QApplication

from core.kiwoom.openapi.client import OpenApiClient
from core.kiwoom.openapi.input_value import InputValue
from core.kiwoom.openapi.account_info_type import AccountInfoType


@pytest.fixture(scope="session")
def application():
    return QApplication(sys.argv)


@pytest.fixture(scope="module")
def client(application):
    client = OpenApiClient()
    client.connect()
    return client


def test_get_connect_state(client):
    assert client.get_connect_state()


def test_get_login_info(client):
    # When
    accounts = client.get_login_info(AccountInfoType.ACCLIST)

    # Then
    assert len(accounts) > 0


def test_comm_rq_data(client):
    input_values = [
        InputValue(s_id='종목코드', s_value='005930'),
        InputValue(s_id='기준일자', s_value='20210424'),
        InputValue(s_id='수정주가구분', s_value=1),
    ]
    rqname = 'opt10081_req'
    trcode = 'opt10081'
    item_key_pair = {
        '일자': 'date',
        '시가': 'open',
        '고가': 'high',
        '저가': 'low',
        '현재가': 'close',
        '거래량': 'volume',
        '거래대금': 'trading_value'
    }
    response = client.comm_rq_data(
        input_values, rqname, trcode, 0, item_key_pair)

    assert len(response.rows) > 0
    assert response.has_next


def test_comm_rq_data_repeat(client):
    input_values = [
        InputValue(s_id='종목코드', s_value='005930'),
        InputValue(s_id='기준일자', s_value='20210424'),
        InputValue(s_id='수정주가구분', s_value=1),
    ]
    rqname = 'opt10081_req'
    trcode = 'opt10081'
    item_key_pair = {
        '일자': 'date',
        '시가': 'open',
        '고가': 'high',
        '저가': 'low',
        '현재가': 'close',
        '거래량': 'volume',
        '거래대금': 'trading_value'
    }
    response = client.comm_rq_data_repeat(
        input_values, rqname, trcode, item_key_pair)

    assert len(response.rows) > 0
