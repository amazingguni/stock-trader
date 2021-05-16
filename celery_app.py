from celery import Celery

from app import app as flask_app
from container import container
TASKS_MODULE = [
    "tasks.stock_summaries",
]


def make_celery(flask_app):
    celery = Celery(
        flask_app.import_name,
        backend=flask_app.config['CELERY_RESULT_BACKEND'],
        broker=flask_app.config['CELERY_BROKER_URL'],
        include=TASKS_MODULE
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                from tasks import stock_summaries
                container.wire(modules=[stock_summaries])
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = make_celery(flask_app)
app.autodiscover_tasks()
