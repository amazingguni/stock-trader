import os
from .config import Config


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ADMIN_DEFAULT_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    MONGODB_SETTINGS = {
        'db': 'stock-trader',
        'host': 'localhost',
        'port': 27017
    }
