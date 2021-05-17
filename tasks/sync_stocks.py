from dependency_injector.wiring import inject, Provide

from celery_app import app
from container import Container

from core.stock.application.sync_stock_service import SyncStockService


@app.task(bind=True)
@inject
def sync(self,
         sync_stock_service: SyncStockService = Provide[Container.sync_stock_service]):
    sync_stock_service.sync()
