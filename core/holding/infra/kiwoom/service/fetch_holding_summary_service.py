from core.external.kiwoom import OpenApiClient, InputValue

from core.holding.domain import HoldingSummary, Holding
from core.holding.domain.service import FetchHoldingSummaryService


class KiwoomFetchHoldingSummaryService(FetchHoldingSummaryService):
    def __init__(self, openapi_client: OpenApiClient):
        self.openapi_client = openapi_client

    def fetch(self, account_number: str):
        summary = self.__fetch_total_summary(account_number)
        summary.holdings = self.__fetch_holdings(account_number)
        return summary

    def __fetch_total_summary(self, account_number: str):
        input_values = [
            InputValue(s_id='계좌번호', s_value=account_number),
        ]
        row_keys = ['총매입금액', '총평가금액', '총평가손익금액',
                    '총수익률(%)', '추정예탁자산']
        trcode = 'opw00018'
        response = self.openapi_client.comm_rq_single_data(
            trcode, input_values, row_keys)

        for row in response.rows:
            return HoldingSummary(
                account_number=account_number,
                total_purchase_price=int(row['총매입금액']),
                total_eval_price=int(row['총평가금액']),
                total_eval_profit_loss_price=int(row['총평가손익금액']),
                total_earning_rate=float(row['총수익률(%)']),
                estimated_deposit=int(row['추정예탁자산']))
        return None

    def __fetch_holdings(self, account_number: str):
        input_values = [
            InputValue(s_id='계좌번호', s_value=account_number),
        ]
        row_keys = ['종목번호', '종목명', '보유수량', '매입가',
                    '현재가', '평가손익',  '수익률(%)', '매입금액']
        trcode = 'opw00018'
        response = self.openapi_client.comm_rq_data_repeat(
            trcode, input_values, row_keys)

        holdings = []
        for row in response.rows:
            holding = Holding(
                stock_code=row['종목번호'],
                stock_name=row['종목명'],
                quantity=int(row['보유수량']),
                purchase_price=int(row['매입가']),
                current_price=int(row['현재가']),
                eval_profit_loss_price=int(row['평가손익']),
                earning_rate=float(row['수익률(%)']),
                total_purchase_price=int(row['매입금액']))
            holdings.append(holding)
        return holdings
