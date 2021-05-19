from core.deposit.domain.deposit import Deposit


class DepositRepository:
    def save(self, deposit: Deposit):
        deposit.save()
