from http import HTTPStatus
from dependency_injector.wiring import inject, Provide
from flask import Blueprint, Response, redirect, url_for


bp = Blueprint('stock', __name__,
               template_folder='templates', static_folder="static", url_prefix='/stock/')


@bp.route('/sync/', methods=['POST', ])
def sync():
    from tasks.sync_stocks import sync
    job = sync().delay()
    return redirect(url_for('crawl-admin.job_status', job_id=job.id))


@bp.route('/crawl/all-daily-summaries/', methods=['POST', ])
def crawl_all_daily_summaries():
    from tasks.stock_summaries import crawl_daily_stock_all
    job = crawl_daily_stock_all.delay()
    return redirect(url_for('crawl-admin.job_status', job_id=job.id))
