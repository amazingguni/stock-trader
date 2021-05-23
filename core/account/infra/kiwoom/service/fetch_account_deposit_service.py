from core.account.domain import Account, Deposit
from core.account.domain.service import FetchAccountDepositService

from core.external.kiwoom import OpenApiClient, InputValue


class KiwoomFetchAccountDepositService(FetchAccountDepositService):
    def __init__(self, client: OpenApiClient):
        self.client = client

    def fetch(self, account: Account):
        input_values = [
            InputValue(s_id='계좌번호', s_value=account.number),
            InputValue(s_id='비밀번호입력매체구분', s_value=00),
            # 조회구분 = 1:추정조회, 2:일반조회
            InputValue(s_id='조회구분', s_value=1),
        ]
        row_keys = ['예수금', 'd+2출금가능금액']
        trcode = 'opw00001'
        response = self.client.comm_rq_single_data(
            trcode, input_values, row_keys)

        deposits = []
        for row in response.rows:
            deposit = Deposit(
                d2_withdrawable_deposit=int(row['d+2출금가능금액']),
                deposit=int(row['예수금']))
            deposits.append(deposit)
        return deposits[0] if deposits else None