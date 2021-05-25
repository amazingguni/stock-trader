from core.holding.domain import HoldingSummary
from core.holding.domain.repository import HoldingSummaryRepository


def test_save(mongo_connection):
    summary = HoldingSummary(account_number='11111111', total_purchase_price=10000,
                             total_eval_price=9000, total_eval_profit_loss_price=1000,
                             total_earning_rate=91.1, estimated_deposit=10000)

    HoldingSummaryRepository().save(summary)

    assert HoldingSummary.objects.count() == 1


def test_find_latest_by_account(mongo_connection):
    HoldingSummary(account_number='11111111', total_purchase_price=10000,
                   total_eval_price=9000, total_eval_profit_loss_price=1000,
                   total_earning_rate=91.1, estimated_deposit=10000)
    HoldingSummary(account_number='11111111', total_purchase_price=10000,
                   total_eval_price=9000, total_eval_profit_loss_price=1000,
                   total_earning_rate=91.1, estimated_deposit=10000)
    HoldingSummary(account_number='11111111', total_purchase_price=10000,
                   total_eval_price=9000, total_eval_profit_loss_price=1000,
                   total_earning_rate=91.1, estimated_deposit=10000)
