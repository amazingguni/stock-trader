class KiwoomHoldingsService:
    def fetch(self):
        input_values = [
            InputValue(s_id='계좌번호', s_value=self.account_numbers[0]),
            # InputValue(s_id='비밀번호입력매체구분', s_value=00),
            # 조회구분 = 1:추정조회, 2:일반조회
            # InputValue(s_id='조회구분', s_value=1),
        ]
