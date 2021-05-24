from core.account.domain import Account, SECURITIES_COMPANY_KIWOOM
from core.account.domain.service import FetchAccountService

from core.external.kiwoom import OpenApiClient, AccountInfoType, IMITATION_SERVER


class KiwoomFetchAccountService(FetchAccountService):
    def __init__(self, openapi_client: OpenApiClient):
        self.openapi_client = openapi_client

    def fetch_all(self):
        server_gubun = self.openapi_client.get_login_info(
            AccountInfoType.GetServerGubun)
        is_real = int(server_gubun) != IMITATION_SERVER
        client_ret = self.openapi_client.get_login_info(
            AccountInfoType.ACCLIST)

        accounts = []
        for account_number in client_ret.split(';'):
            if not account_number:
                continue

            account = Account(number=account_number,
                              securities_company=SECURITIES_COMPANY_KIWOOM,
                              real=is_real,
                              primary=False)
            accounts.append(account)
        return accounts 
