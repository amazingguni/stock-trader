from core.account.domain import Deposit


class DepositRepository:
    def save(self, deposit: Deposit):
        deposit.save()
