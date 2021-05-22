import sys
import pytest


from core.external.kiwoom import InputValue, AccountInfoType

pytestmark = [pytest.mark.kiwoom, pytest.mark.slow]


def test_get_connect_state(openapi_client):
    assert openapi_client.get_connect_state()


def test_get_login_info(openapi_client):
    # When
    ret = openapi_client.get_login_info(AccountInfoType.ACCLIST)

    # Then
    assert len(ret) > 0


def test_comm_rq_data(openapi_client):
    input_values = [
        InputValue(s_id='종목코드', s_value='005930'),
        InputValue(s_id='기준일자', s_value='20210424'),
        InputValue(s_id='수정주가구분', s_value=1),
    ]
    trcode = 'opt10081'
    row_keys = ['일자', '시가', '고가', '저가', '현재가', '거래량', ]
    response = openapi_client.comm_rq_data(
        trcode, input_values, 0, row_keys)

    assert len(response.rows) > 0
    assert response.has_next


def test_comm_rq_data_repeat(openapi_client):
    input_values = [
        InputValue(s_id='종목코드', s_value='035720'),
        InputValue(s_id='기준일자', s_value='20210424'),
        InputValue(s_id='수정주가구분', s_value=1),
    ]
    trcode = 'opt10081'
    row_keys = ['일자', '시가', '고가', '저가', '현재가', '거래량', ]
    response = openapi_client.comm_rq_data_repeat(
        trcode, input_values, row_keys)

    assert len(response.rows) > 0
