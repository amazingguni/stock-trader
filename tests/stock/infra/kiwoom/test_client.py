import pytest

from core.stock.infra.kiwoom.openapi.input_value import InputValue
from core.stock.infra.kiwoom.openapi.account_info_type import AccountInfoType

pytestmark = [pytest.mark.kiwoom, pytest.mark.slow]


def test_get_connect_state(client):
    assert client.get_connect_state()


def test_get_login_info(client):
    # When
    ret = client.get_login_info(AccountInfoType.ACCLIST)

    # Then
    assert len(ret) > 0


def test_comm_rq_data(client):
    input_values = [
        InputValue(s_id='종목코드', s_value='005930'),
        InputValue(s_id='기준일자', s_value='20210424'),
        InputValue(s_id='수정주가구분', s_value=1),
    ]
    trcode = 'opt10081'
    item_key_pair = {
        '일자': 'date',
        '시가': 'open',
        '고가': 'high',
        '저가': 'low',
        '현재가': 'close',
        '거래량': 'volume',
    }
    response = client.comm_rq_data(
        trcode, input_values, 0, item_key_pair)

    assert len(response.rows) > 0
    assert response.has_next


def test_comm_rq_data_repeat(client):
    input_values = [
        InputValue(s_id='종목코드', s_value='035720'),
        InputValue(s_id='기준일자', s_value='20210424'),
        InputValue(s_id='수정주가구분', s_value=1),
    ]
    trcode = 'opt10081'
    item_key_pair = {
        '일자': 'date',
        '시가': 'open',
        '고가': 'high',
        '저가': 'low',
        '현재가': 'close',
        '거래량': 'volume',
    }
    response = client.comm_rq_data_repeat(
        trcode, input_values, item_key_pair)

    assert len(response.rows) > 0
