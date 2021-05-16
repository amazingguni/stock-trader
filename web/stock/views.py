from http import HTTPStatus
from dependency_injector.wiring import inject, Provide
from flask import Blueprint, Response, redirect, url_for

from container import Container
from core.stock.application.sync_stock_service import SyncStockService
from core.stock.application.crawl_daily_stock_summary_service import CrawlDailyStockSummaryService


bp = Blueprint('stock', __name__,
               template_folder='templates', static_folder="static", url_prefix='/stock/')


@bp.route('/sync/', methods=['POST', ])
@inject
def sync(
        sync_stock_service: SyncStockService = Provide[Container.sync_stock_service]):
    sync_stock_service.sync()
    return redirect(url_for('stock-admin.index_view'))


@bp.route('/crawl/all-daily-summaries/', methods=['POST', ])
def crawl_all_daily_summaries():
    from tasks.stock_summaries import crawl_daily_stock_all
    job = crawl_daily_stock_all.delay()
    return redirect(url_for('crawl-admin.job_status', job_id=job.id))
