from core.account.domain import Account
from core.holding.domain import HoldingSummary


def test_constructor(mongo_connection):
    account = Account(number='11111111')
    HoldingSummary(account=account, total_purchase_price=10000,
                   total_eval_price=9000, total_eval_profit_loss_price=1000,
                   total_earning_rate=91.1, estimated_deposit=10000)
