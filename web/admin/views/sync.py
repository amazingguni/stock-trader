import json

from flask import request, redirect, url_for
from flask_admin import BaseView, expose
from celery.result import AsyncResult

from tasks.stock_tasks import sync_stocks
from tasks.securities_tasks import sync_account, sync_all_daily_summaries, sync_holding_summary


class SyncView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/sync.html.j2')

    @expose('/progress')
    def progress(self):
        from celery_app import app as celery_app
        job_id = request.values.get('job_id')
        job = AsyncResult(job_id, app=celery_app)

        return json.dumps(dict(
            state=job.state,
            message=job.result.get(
                'message') if job.result else '',
            current=job.result.get('current') if job.result else 0,
            total=job.result.get('total') if job.result else 10,
        ))

    @expose('/job-status')
    def job_status(self):
        job_id = request.args.get('job_id')
        return self.render('admin/job_status.html.j2', job_id=job_id)

    @expose('/stock', methods=['POST'])
    def sync_stock(self):
        job = sync_stocks.delay()
        job.wait(timeout=120)
        return redirect(url_for('stock-admin.index_view'))

    @expose('/account', methods=['POST'])
    def sync_account(self):
        job = sync_account.delay()
        job.wait(timeout=30)
        return redirect(url_for('account-admin.index_view'))

    @expose('/all-daily-summaries', methods=['POST'])
    def sync_all_daily_summaries(self):
        job = sync_all_daily_summaries.delay()
        return redirect(url_for('sync-admin.job_status', job_id=job.id))

    @expose('/holding-summary', methods=['POST'])
    def sync_holding_summary(self):
        job = sync_holding_summary.delay()
        job.wait(timeout=30)
        return redirect(url_for('holding-summary-admin.index_view'))
