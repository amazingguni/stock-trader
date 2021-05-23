import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'sqlite:///db.sqlite')
    ADMIN_DEFAULT_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'


def get_config_by_env():
    config_name = os.environ.get('CONFIG', 'development')
    return get_config_by_str(config_name)


def get_config_by_str(config_name):
    from .development import DevelopmentConfig
    from .testing import TestingConfig
    from .production import ProductionConfig
    if config_name == 'development':
        return DevelopmentConfig
    if config_name == 'testing':
        return TestingConfig
    if config_name == 'production':
        return ProductionConfig
    raise ValueError('Given config_name is invalid')
