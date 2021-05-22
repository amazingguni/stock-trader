from core.account.domain import Deposit
from core.account.domain.repository import DepositRepository


def test_save(mongo_connection):
    deposit = Deposit(deposit=1000000, d2_withdrawable_deposit=2000000)

    DepositRepository().save(deposit)

    assert Deposit.objects.count() == 1
