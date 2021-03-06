import importlib
from celery import Celery
from celery.schedules import crontab
import mongoengine


from container import Container
from config import get_config_by_env

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
    celery.conf.update(
        beat_schedule={
            'sync_stocks': {
                'task': 'tasks.stock_tasks.sync_stocks',
                'schedule': crontab(hour='18')
            },
            'sync_account': {
                'task': 'tasks.securities_tasks.sync_account',
                'schedule': crontab(hour='18')
            },
            'sync_holding_summary': {
                'task': 'tasks.securities_tasks.sync_holding_summary',
                'schedule': crontab(hour='18')
            },
            'sync_all_daily_summaries': {
                'task': 'tasks.securities_tasks.sync_all_daily_summaries',
                'schedule': crontab(hour='18')
            }
        }
    )
    mongoengine.connect(
        db=config.MONGODB_SETTINGS['db'],
        host=config.MONGODB_SETTINGS['host'],
        port=config.MONGODB_SETTINGS['port'])
    container = Container()

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
