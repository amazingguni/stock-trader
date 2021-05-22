from enum import Enum, auto

IMITATION_SERVER = 1


class AccountInfoType(Enum):
    '''보유계좌 갯수를 반환'''
    ACCOUNT_CNT = auto()
    '''구분자 ';'로 연결된 보유계좌 목록을 반환'''
    ACCLIST = auto()
    '''사용자 ID를 반환'''
    USER_ID = auto()
    '''사용자 이름을 반환'''
    USER_NAME = auto()
    '''접속서버 구분을 반환(1 : 모의투자, 나머지 : 실거래서버)'''
    SetServerGubun = auto()
    '''키보드 보안 해지여부를 반환(0 : 정상, 1 : 해지)'''
    KEY_BSECGB = auto()
    '''방화벽 설정여부를 반환(0 : 미설정, 1 : 설정, 2 : 해지)'''
    FIREW_SECGB = auto()
