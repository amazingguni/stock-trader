from core.account.domain import Account
from core.stock.domain import Stock
from core.holding.domain import Holding


def test_constructor():
    account = Account(number='11111111')
    stock = Stock(market=Stock.MARKET_KOSDAQ, name='우리회사', code='111111')
    Holding(
        account=account,
        stock=stock,
        quantity=10,
        purchase_price=1000,
        current_price=1101,
        eval_profit_loss_price=101,
        earning_rate=10.1,
        total_purchase_price=10000
    )
