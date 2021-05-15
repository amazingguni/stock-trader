from http import HTTPStatus
from dependency_injector.wiring import inject, Provide

from flask import Blueprint, Response

from container import Container
from core.stock.application.sync_stock_service import SyncStockService


bp = Blueprint('stock', __name__,
               template_folder='templates', static_folder="static", url_prefix='/stock/')


@bp.route('/sync/', methods=['POST', ])
@inject
def sync(
        sync_stock_service: SyncStockService = Provide[Container.sync_stock_service]):
    sync_stock_service.sync()
    return Response(status=HTTPStatus.OK)
