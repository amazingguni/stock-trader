from core.account.domain import Deposit


def test_deposit():
    Deposit(deposit=1000000, d2_withdrawable_deposit=2000000)
