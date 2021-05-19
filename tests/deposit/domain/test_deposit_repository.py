from core.deposit.domain.deposit import Deposit
from core.deposit.domain.deposit_repository import DepositRepository


def test_save(mongo_connection):
    deposit = Deposit(deposit=1000000, d2_withdrawable_deposit=2000000)

    DepositRepository().save(deposit)

    assert Deposit.objects.count() == 1
