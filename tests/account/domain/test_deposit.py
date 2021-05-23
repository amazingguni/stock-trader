from core.account.domain import Account, Deposit


def test_deposit(mongo_connection):
    account = Account(number='11111111').save()
    Deposit(account=account, deposit=1000000, d2_withdrawable_deposit=2000000)
