from .config import Config


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'stock-trader',
        'host': 'localhost',
        'port': 27017
    }
