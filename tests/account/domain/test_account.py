from core.account.domain import Account


def test_model():
    Account(securities_company='키움증권',
            number='12345678', real=True, primary=True)
