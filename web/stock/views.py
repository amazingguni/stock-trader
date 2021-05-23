from flask import Blueprint, redirect, url_for
from tasks.stock_tasks import sync_stocks

bp = Blueprint('stock', __name__,
               template_folder='templates', static_folder="static", url_prefix='/stock/')


@bp.route('/sync/', methods=['POST', ])
def sync():

    job = sync_stocks.delay()
    return redirect(url_for('stock-admin.index_view', job_id=job.id))


@bp.route('/crawl/all-daily-summaries/', methods=['POST', ])
def crawl_all_daily_summaries():
    from tasks.securities_tasks import sync_daily_stock_all
    job = sync_daily_stock_all.delay()
    return redirect(url_for('crawl-admin.job_status', job_id=job.id))
