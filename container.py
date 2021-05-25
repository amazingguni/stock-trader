from dependency_injector import containers, providers

from PyQt5.QtWidgets import QApplication

from core.external.kiwoom import OpenApiClient

from core.stock.application.sync_stock_service import SyncStockService
from core.stock.domain.repository.stock_repository import StockRepository

from core.account.domain.repository import AccountRepository, DepositRepository
from core.account.infra.kiwoom.service import KiwoomFetchAccountService, KiwoomFetchAccountDepositService
from core.account.application import SyncAccountService


from core.summary.application import SyncDailyStockSummaryService, DeleteDailyStockSummaryService
from core.summary.domain.repository import DailyStockSummaryRepository
from core.summary.infra.kiwoom.service import KiwoomFetchDailyStockSummaryService


def create_openapi_client():
    if not QApplication.instance():
        qapp = QApplication([])
    openapi_client = OpenApiClient()
    openapi_client.connect()
    yield openapi_client
    qapp.exit()


class Container(containers.DeclarativeContainer):
    openapi_client = providers.Resource(create_openapi_client)

    account_repository = providers.Factory(AccountRepository)
    deposit_repository = providers.Factory(DepositRepository)
    fetch_account_service = providers.Factory(
        KiwoomFetchAccountService, openapi_client=openapi_client)
    fetch_account_deposit_service = providers.Factory(
        KiwoomFetchAccountDepositService, openapi_client=openapi_client)
    sync_account_service = providers.Factory(
        SyncAccountService, account_repository=account_repository,
        deposit_repository=deposit_repository,
        fetch_account_service=fetch_account_service,
        fetch_account_deposit_service=fetch_account_deposit_service)

    stock_repository = providers.Factory(StockRepository)
    sync_stock_service = providers.Factory(
        SyncStockService, stock_repository=stock_repository)

    daily_stock_summary_repository = providers.Factory(
        DailyStockSummaryRepository)
    fetch_daily_stock_summary_service = providers.Factory(
        KiwoomFetchDailyStockSummaryService, openapi_client=openapi_client
    )
    sync_daily_stock_summary_service = providers.Factory(
        SyncDailyStockSummaryService,
        fetch_daily_stock_summary_service=fetch_daily_stock_summary_service,
        stock_repository=stock_repository,
        daily_stock_summary_repository=daily_stock_summary_repository)
    delete_daily_stock_summary_service = providers.Factory(
        DeleteDailyStockSummaryService,
        stock_repository=stock_repository,
        daily_stock_summary_repository=daily_stock_summary_repository)
