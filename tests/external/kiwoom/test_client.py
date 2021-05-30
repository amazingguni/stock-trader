from unittest import mock
import pytest

from core.external.kiwoom import InputValue, AccountInfoType, \
    BiddingType, OrderType, ChejanType, OrderConcludedEvent, ConclusionType

pytestmark = [pytest.mark.kiwoom, pytest.mark.slow]

@pytest.fixture(scope='session')
def account_number(openapi_client):
    ret = openapi_client.get_login_info(AccountInfoType.ACCLIST)
    return ret.split(';')[0]
    
def test_get_connect_state(openapi_client):
    assert openapi_client.get_connect_state()



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

def test_send_order(openapi_client, account_number):
    openapi_client.send_order(
        account_number=account_number, 
        order_type=OrderType.CREATE_BID,
        stock_code='035720',
        quantity=3,
        price=4000,
        bidding_type=BiddingType.PENDING)

@mock.patch('core.external.kiwoom.client.OpenApiClient.get_chejan_data')
def test_order_concluded_event(mock_get_chejan_data, openapi_client, account_number):
    def side_effect(fid):
        if fid == ChejanType.CONCLUSION_NUMBER:
            return 1000
        if fid== ChejanType.ACCOUNT_NUMBER:
            return '11115455'
        if fid == ChejanType.ORDER_NUMBER:
            return 1
        if fid == ChejanType.STOCK_CODE:
            return '152555'
        if fid == ChejanType.ORDERED_QUANTITY:
            return 5
        if fid == ChejanType.CONCLUDED_QUANTITY:
            return 3
        if fid == ChejanType.BALANCED_QUANTITY:
            return 2
        if fid == ChejanType.ORDER_TYPE:
            return '+매수'
        if fid == ChejanType.CONCLUDED_AT:
            return '2010년xx시'
        if fid == ChejanType.CONCLUDED_PRICE:
            return 1403
        
    mock_get_chejan_data.side_effect = side_effect
    mock_handler = mock.MagicMock()
    mock_handler.handle.return_value = None

    openapi_client.register_order_concluded_handler(mock_handler)
    openapi_client.OnReceiveChejanData.emit('0', 5, '12;123')

    mock_handler.handle.assert_called()
    args = mock_handler.handle.call_args
    called_event = args[0][0]
    assert called_event.conclusion_type == ConclusionType.BID
    assert called_event.conclusion_number == 1000
    assert called_event.stock_code == '152555'
    assert called_event.account_number == '11115455'
    assert called_event.concluded_price == 1403
    assert called_event.ordered_quantity == 5
    assert called_event.concluded_quantity == 3
    assert called_event.balanced_quantity == 2


