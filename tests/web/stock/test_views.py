import pytest
from time import sleep
from http import HTTPStatus
from flask import url_for

from core.stock.domain.stock import Stock


@pytest.mark.slow
def test_sync(client):
    response = client.post(url_for('stock.sync'))

    # Then
    assert response.status_code == HTTPStatus.OK

    # Then
    assert Stock.objects.count() > 0
