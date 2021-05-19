import sys
import pytest
from PyQt5.QtWidgets import QApplication

from core.stock.infra.kiwoom.openapi.client import OpenApiClient


@pytest.fixture(scope="package")
def application():
    app = QApplication(sys.argv)
    yield app
    app.exit()


@pytest.fixture(scope="package")
def client(application):
    _client = OpenApiClient()
    _client.connect()
    yield _client
