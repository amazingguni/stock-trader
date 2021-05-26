from core.holding.domain import HoldingSummary, Holding


def test_constructor(mongo_connection):
    holdings = [
        Holding(
            stock_name='우리회사',
            stock_code='111111',
            quantity=10,
            purchase_price=1000,
            current_price=1101,
            eval_profit_loss_price=101,
            earning_rate=10.1,
            total_purchase_price=10000
        ),
        Holding(
            stock_name='삼성전자',
            stock_code='222222',
            quantity=10,
            purchase_price=1000,
            current_price=1101,
            eval_profit_loss_price=101,
            earning_rate=10.1,
            total_purchase_price=10000
        )
    ]
    HoldingSummary(account_number='11111111', total_purchase_price=10000,
                   total_eval_price=9000, total_eval_profit_loss_price=1000,
                   total_earning_rate=91.1, estimated_deposit=10000,
                   holdings=holdings).save()
