import sys
from dependency_injector import containers, providers
from flask import Flask
from PyQt5.QtWidgets import QApplication

from core.stock.application.crawl_daily_stock_summary_service import CrawlDailyStockSummaryService
from core.stock.application.sync_stock_service import SyncStockService
from core.stock.domain.repository.daily_stock_summary_repository import DailyStockSummaryRepository
from core.stock.domain.repository.stock_repository import StockRepository
from core.stock.infra.kiwoom.connector import KiwoomConnector

from core.deposit.domain.deposit_repository import DepositRepository


class Container(containers.DeclarativeContainer):
    app = providers.Dependency(instance_of=Flask)
    q_application = providers.Singleton(QApplication, sys.argv)
    stock_connector = providers.Singleton(KiwoomConnector, q_application)

    stock_repository = providers.Factory(StockRepository)
    daily_stock_summary_repository = providers.Factory(
        DailyStockSummaryRepository)
    deposit_repository = providers.Factory(DepositRepository)

    sync_stock_service = providers.Factory(
        SyncStockService, stock_repository=stock_repository)
    crawl_daily_stock_summary_service = providers.Factory(
        CrawlDailyStockSummaryService, stock_connector=stock_connector,
        stock_repository=stock_repository,
        daily_stock_summary_repository=daily_stock_summary_repository)


container = Container()
