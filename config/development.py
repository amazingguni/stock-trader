import os
from .config import Config


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ADMIN_DEFAULT_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
    MONGODB_SETTINGS = {
        'db': 'dev-stock-trader',
        'host': 'localhost',
        'port': 27017
    }
