from enum import Enum


class ChejanType(Enum):
    '''거래구분(혹은 호가구분)'''
    '''계좌번호'''
    ACCOUNT_NUMBER = 9201
    '''주문번호'''
    ORDER_NUMBER = 9203
    '''종목코드'''
    STOCK_CODE = 9001
    '''주문수량'''
    ORDERED_QUANTITY = 900
    '''주문가격'''
    ORDERED_PRICE = 901
    '''미체결수량'''
    BALANCED_QUANTITY = 902
    '''원주문번호'''
    ORIGIN_ORDER_NUMBER = 904

    '''주문 구분, "+매수" or "-매도"'''
    ORDER_TYPE = 905

    '''체결 번호'''
    CONCLUSION_NUMBER = 909

    # '''체결가'''
    # CHEJAN_PRICE = 910
    '''현재가, 체결가, 실시간종가'''
    CONCLUDED_PRICE = 10

    '''체결량'''
    CONCLUDED_QUANTITY = 911

    '''주문/체결시간'''
    CONCLUDED_AT = 908
