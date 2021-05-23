# from celery import current_task
from dependency_injector.wiring import inject, Provide
from container import Container
from celery_app import app


@app.task(bind=True)
@inject
def sync_account(self,
                 sync_account_service=Provide[Container.sync_account_service]):
    sync_account_service.sync()


@app.task(bind=True)
@inject
def sync_all_daily_summaries(self,
                             sync_daily_stock_summary_service=Provide[Container.sync_daily_stock_summary_service]):
    stock_cnt = 999
    for i, total, stock in sync_daily_stock_summary_service.sync_all():
        stock_cnt = total
        self.update_state(
            state='PROGRESS',
            meta={'message': stock.name,
                  'current': i + 1, 'total': total})
        print(f'{stock.name}({i + 1}/{stock_cnt})')

    return {'message': 'DONE', 'current': stock_cnt, 'total': stock_cnt}
