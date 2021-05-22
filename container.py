from dependency_injector import containers, providers

from core.external.kiwoom import OpenApiClient

from core.stock.application.sync_stock_service import SyncStockService
from core.stock.domain.repository.stock_repository import StockRepository

from core.account.domain.repository import DepositRepository
from core.account.infra.kiwoom.service import KiwoomFetchAccountService, KiwoomFetchAccountDepositService

from core.summary.application import SyncDailyStockSummaryService
from core.summary.domain.repository import DailyStockSummaryRepository
from core.summary.infra.kiwoom.service import KiwoomFetchDailyStockSummaryService


class Container(containers.DeclarativeContainer):
    openapi_client = providers.Dependency(instance_of=OpenApiClient)
    stock_repository = providers.Factory(StockRepository)

    deposit_repository = providers.Factory(DepositRepository)
    fetch_account_service = providers.Factory(
        KiwoomFetchAccountService, openapi_client=openapi_client)
    fetch_account_deposit_service = providers.Factory(
        KiwoomFetchAccountDepositService, openapi_client=openapi_client)

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
