import os
from .config import Config


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ADMIN_DEFAULT_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
