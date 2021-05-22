
class KiwoomError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg


class ConnectFailedError(KiwoomError):
    def __init__(self):
        super().__init__('접속 실패')


class TransactionFailedError(KiwoomError):
    def __init__(self):
        super().__init__('트랜젝션 실패')


class RateLimitExceeded(KiwoomError):
    def __init__(self):
        super().__init__('요청제한 횟수를 초과하였습니다.')
