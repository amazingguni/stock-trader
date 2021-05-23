# from celery import current_task
from dependency_injector.wiring import inject, Provide
from container import Container
from celery_app import app

from core.summary.application import SyncDailyStockSummaryService
from core.account.domain.service import FetchAccountDepositService


@app.task(bind=True)
@inject
def sync_daily_stock_all(self,
                         sync_daily_stock_summary_service: SyncDailyStockSummaryService = Provide[Container.sync_daily_stock_summary_service]):
    stock_cnt = 999
    for i, total, stock in sync_daily_stock_summary_service.sync_all():
        stock_cnt = total
        self.update_state(
            state='PROGRESS',
            meta={'message': stock.name,
                  'current': i + 1, 'total': total})
        print(f'{stock.name}({i + 1}/{stock_cnt})')

    return {'message': 'DONE', 'current': stock_cnt, 'total': stock_cnt}


@app.task(bind=True)
@inject
def fetch_account_deposit(self,
                          fetch_account_deposit_service: FetchAccountDepositService
                          = Provide[Container.fetch_account_deposit_service]):
    deposit = fetch_account_deposit_service.fetch()
    return {
        'deposit': deposit.deposit,
        'd2_withdrawable_deposit': deposit.d2_withdrawable_deposit,
    }
