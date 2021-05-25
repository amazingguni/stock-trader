from core.holding.domain import HoldingSummary


def test_constructor(mongo_connection):
    HoldingSummary(account_number='11111111', total_purchase_price=10000,
                   total_eval_price=9000, total_eval_profit_loss_price=1000,
                   total_earning_rate=91.1, estimated_deposit=10000)
