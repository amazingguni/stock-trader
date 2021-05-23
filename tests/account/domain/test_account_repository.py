from core.account.domain import Account
from core.account.domain.repository import AccountRepository


def test_save(mongo_connection):
    account = Account(securities_company='키움증권',
                      number='12345678', real=True, primary=True)

    AccountRepository().save(account)

    assert Account.objects.count() == 1
    assert Account.objects.first().number == '12345678'


def test_save_all(mongo_connection):
    account_a = Account(securities_company='키움증권',
                        number='12345678', real=True, primary=True)
    account_b = Account(securities_company='키움증권',
                        number='98712345', real=True, primary=False)

    AccountRepository().save_all([account_a, account_b])

    assert Account.objects.count() == 2


def test_update(mongo_connection):
    account = Account(securities_company='키움증권',
                      number='12345678', real=False, primary=True)
    account.save()

    AccountRepository().update(account, {'real': True, 'primary': False})

    ret_account = Account.objects.first()
    assert ret_account.real
    assert not ret_account.primary


def test_find_by_account_number(mongo_connection):
    imitation_account = Account(securities_company='키움증권',
                                number='12345678', real=False, primary=True).save()
    real_account = Account(securities_company='우리증권',
                           number='00000000', real=True, primary=True).save()

    repository = AccountRepository()
    assert repository.find_by_account_number(
        number='12345678') == imitation_account

    assert repository.find_by_account_number(
        number='00000000') == real_account

    assert not repository.find_by_account_number(number='INVALID')


def test_find_primary_account(mongo_connection):
    imitation_primary_account = Account(securities_company='키움증권',
                                        number='12345678', real=False, primary=True).save()
    real_primary_account = Account(securities_company='우리증권',
                                   number='00000000', real=True, primary=True).save()
    Account(securities_company='우리증권',
            number='11111111', real=True, primary=False).save()

    repository = AccountRepository()

    assert repository.find_primary_account()
    assert repository.find_primary_account(
        {'real': False}) == imitation_primary_account
    assert repository.find_primary_account(
        {'real': True}) == real_primary_account
