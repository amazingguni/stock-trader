# from celery import current_task
from dependency_injector.wiring import inject, Provide
from celery_app import app

from container import Container

from core.stock.application.crawl_daily_stock_summary_service import CrawlDailyStockSummaryService
from core.stock.domain.repository.stock_repository import StockRepository


@app.task(bind=True)
@inject
def crawl_daily_stock_all(self,
                          stock_repository: StockRepository = Provide[Container.stock_repository],
                          crawl_daily_stock_service: CrawlDailyStockSummaryService = Provide[Container.crawl_daily_stock_summary_service]):
    stocks = stock_repository.find_all()
    total = len(stocks)
    for i, stock in enumerate(stocks):
        print(stock.name)
        crawl_daily_stock_service.crawl(stock.code)
        self.update_state(
            state='PROGRESS',
            meta={'message': stock.name,
                  'current': i + 1, 'total': total})

    return {'message': 'DONE', 'current': total, 'total': total}
