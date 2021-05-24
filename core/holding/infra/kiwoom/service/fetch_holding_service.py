from core.external.kiwoom import OpenApiClient, InputValue

from core.holding.domain import HoldingSummary
from core.holding.domain.service import FetchHoldingService


class KiwoomFetchHoldingService(FetchHoldingService):
    def __init__(self, openapi_client: OpenApiClient):
        self.openapi_client = openapi_client

    def fetch_summary(self, account_number):
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
                total_purchase_price=int(row['총매입금액']),
                total_eval_price=int(row['총평가금액']),
                total_eval_profit_loss_price=int(row['총평가손익금액']),
                total_earning_rate=float(row['총수익률(%)']),
                estimated_deposit=int(row['추정예탁자산']))
        return None

    def fetch_stocks(self, account_number):
        pass
