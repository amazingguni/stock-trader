from enum import Enum


class BiddingType(Enum):
    '''거래구분(혹은 호가구분)'''
    '''지정가'''
    PENDING = '00'
    '''시장가'''
    MARKET = '03'
    #           05 : 조건부지정가
    #           06 : 최유리지정가
    #           07 : 최우선지정가
    #           10 : 지정가IOC
    #           13 : 시장가IOC
    #           16 : 최유리IOC
    #           20 : 지정가FOK
    #           23 : 시장가FOK
    #           26 : 최유리FOK
    #           61 : 장전시간외종가
    #           62 : 시간외단일가매매
    #           81 : 장후시간외종가
