from unittest import mock

from core.account.domain import Account
from core.holding.domain import HoldingSummary, Holding
from core.holding.application import SyncHoldingSummaryService


def generate_holding(stock_name, stock_code):
    return Holding(
        stock_name=stock_name,
        stock_code=stock_code,
        quantity=10,
        purchase_price=1000,
        current_price=1101,
        eval_profit_loss_price=101,
        earning_rate=10.1,
        total_purchase_price=10000
    )


def test_mock_sync(account_repository, holding_summary_repository):
    account = Account(number='00000000', primary=True).save()
    mock_fetch_holding_summary_service = mock.MagicMock()
    holdings = [
        generate_holding('삼성전자', '111111'),
        generate_holding('우리은행', '222222'),
    ]
    mock_fetch_holding_summary_service.fetch.return_value = HoldingSummary(
        account_number=account.number,
        total_purchase_price=10000,
        total_eval_price=9000, total_eval_profit_loss_price=1000,
        total_earning_rate=91.1, estimated_deposit=10000, holdings=holdings)

    SyncHoldingSummaryService(
        account_repository=account_repository,
        holding_summary_repository=holding_summary_repository,
        fetch_holding_summary_service=mock_fetch_holding_summary_service).sync()

    assert HoldingSummary.objects.count() == 1
    assert HoldingSummary.objects.first().holdings.count() == 2
