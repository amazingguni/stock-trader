from core.account.domain import Account, Deposit
from core.account.domain.repository import DepositRepository


def test_save(mongo_connection):
    account = Account(number='11111111').save()
    deposit = Deposit(account=account, deposit=1000000,
                      d2_withdrawable_deposit=2000000)

    DepositRepository().save(deposit)

    assert Deposit.objects.count() == 1
