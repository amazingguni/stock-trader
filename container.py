from dependency_injector import containers, providers

from flask import Flask

from core.stock.domain.stock_connector import StockConnector
from core.stock.domain.repository.stock_repository import StockRepository
from core.stock.domain.repository.daily_stock_summary_repository import DailyStockSummaryRepository

from core.stock.application.sync_stock_service import SyncStockService
from core.stock.application.crawl_daily_stock_summary_service import CrawlDailyStockSummaryService


class Container(containers.DeclarativeContainer):
    app = providers.Dependency(instance_of=Flask)
    stock_connector = providers.Dependency(instance_of=StockConnector)

    stock_repository = providers.Factory(StockRepository)
    daily_stock_summary_repository = providers.Factory(
        DailyStockSummaryRepository)

    sync_stock_service = providers.Factory(
        SyncStockService, stock_repository=stock_repository)
    crawl_daily_stock_summary_service = providers.Factory(
        CrawlDailyStockSummaryService, stock_connector=stock_connector, daily_stock_summary_repository=daily_stock_summary_repository)
