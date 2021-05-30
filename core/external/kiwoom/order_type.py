from enum import Enum


class OrderType(Enum):
    '''신규매수'''
    CREATE_BID = 1
    '''신규매도'''
    CREATE_ASK = 2
    '''매수취소'''
    CANCEL_BID = 3
    '''매도취소'''
    CANCLE_ASK = 4
    '''매수정정'''
    MODIFY_BID = 5
    '''매도정정'''
    MODIFY_ASK = 6
