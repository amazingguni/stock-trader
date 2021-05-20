from celery import Celery
import mongoengine
from container import Container
from config import get_config_by_env

TASKS_MODULE = [
    "tasks.stock_summaries",
    "tasks.stock",
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
    container = Container()

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            from tasks import stock_summaries
            from tasks import stock
            container.wire(modules=[stock_summaries, stock])
            return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = make_celery()
app.autodiscover_tasks()
