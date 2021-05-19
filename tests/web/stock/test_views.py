import pytest
from time import sleep
from http import HTTPStatus
from flask import url_for

from tests.web.utils import assert_redirect_response


def test_sync(client):
    response = client.post(url_for('stock.sync'))

    # Then
    assert_redirect_response(response, url_for('stock-admin.index_view'))
