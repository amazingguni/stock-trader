import os
from . import Config


class TestingConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'test-stock-trader',
        'host': 'mongomock://localhost',
        'port': 27017
    }
