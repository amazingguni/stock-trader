import pytest
from time import sleep
from http import HTTPStatus
from flask import url_for

from core.stock.domain.stock import Stock
from tests.web.utils import assert_redirect_response


@pytest.mark.slow
def test_sync(client):
    response = client.post(url_for('stock.sync'))

    # Then
    assert_redirect_response(response, url_for('stock-admin.index_view'))

    # Then
    assert Stock.objects.count() > 0
