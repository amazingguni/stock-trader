import pytest
from mongoengine import connect, disconnect, get_connection


@pytest.fixture(scope='function')
def mongo_connection():
    connect('mongoenginetest', host='mongomock://localhost')
    yield get_connection()
    disconnect()
