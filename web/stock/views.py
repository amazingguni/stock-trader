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
@inject
def crawl_all_daily_summaries(
        crawl_daily_stock_service: CrawlDailyStockSummaryService = Provide[Container.crawl_daily_stock_summary_service]):
    crawl_daily_stock_service.crawl_all()
    return redirect(url_for('stock-admin.index_view'))
