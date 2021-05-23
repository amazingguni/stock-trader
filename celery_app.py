import importlib
import sys
from celery import Celery
import mongoengine

from PyQt5.QtWidgets import QApplication

from container import Container
from config import get_config_by_env
from core.external.kiwoom import OpenApiClient

TASKS_MODULE = [
    "tasks.securities_tasks",
    "tasks.stock_tasks",
]


def make_celery():
    config = get_config_by_env()
    celery = Celery(
        backend=config.CELERY_RESULT_BACKEND,
        broker=config.CELERY_BROKER_URL,
        include=TASKS_MODULE
    )
    mongoengine.connect(
        db=config.MONGODB_SETTINGS['db'],
        host=config.MONGODB_SETTINGS['host'],
        port=config.MONGODB_SETTINGS['port'])
    if not QApplication.instance():
        _ = QApplication(sys.argv)
    container = Container(openapi_client=OpenApiClient())

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            modules = [importlib.import_module(
                full_module_name) for full_module_name in TASKS_MODULE]
            container.wire(modules=modules)
            return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = make_celery()
app.autodiscover_tasks()
