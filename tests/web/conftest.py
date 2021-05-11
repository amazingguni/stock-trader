import os
import pytest
from flask import template_rendered

from app import create_app


@pytest.fixture(scope='session')
def app():
    """ Session wide test 'Flask' application """
    os.environ['CONFIG'] = 'testing'
    _app = create_app()
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def client(app):
    ctx = app.test_request_context()
    ctx.push()
    yield app.test_client()
    ctx.pop()


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
