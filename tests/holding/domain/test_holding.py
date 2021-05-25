from core.holding.domain import Holding


def test_constructor():
    Holding(
        account_number='12412412412',
        stock_name='우리회사',
        stock_code='111111',
        quantity=10,
        purchase_price=1000,
        current_price=1101,
        eval_profit_loss_price=101,
        earning_rate=10.1,
        total_purchase_price=10000
    )
