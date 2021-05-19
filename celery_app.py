from celery import Celery

from container import container
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
