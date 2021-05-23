import typing
from core.account.domain import Account


class AccountRepository:
    def save(self, account: Account):
        account.save()

    def save_all(self, accounts: typing.List[Account]):
        if not accounts:
            return
        Account.objects.insert(accounts)

    def update(self, account: Account, update: typing.Dict[str, typing.Any]):
        account.update(**update)

    def find_by_account_number(self, real: bool, number: str):
        return Account.objects(number=number, real=real).first()

    def find_primary_accounts(self, query: typing.Dict[str, typing.Any] = None):
        query = query if query else {}
        query['primary'] = True
        return list(Account.objects(**query))