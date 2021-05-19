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
    stock_cnt = 999
    for i, total, stock in crawl_daily_stock_service.crawl_all():
        stock_cnt = total
        self.update_state(
            state='PROGRESS',
            meta={'message': stock.name,
                  'current': i + 1, 'total': total})
        print(f'{stock.name}({i + 1}/{stock_cnt})')

    return {'message': 'DONE', 'current': stock_cnt, 'total': stock_cnt}
