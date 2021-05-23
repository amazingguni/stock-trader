import json

from flask import request
from flask_admin import BaseView, expose
from celery.result import AsyncResult


class CrawlView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/crawl.html.j2')

    @expose('/progress')
    def progress(self):
        from celery_app import app as celery_app
        job_id = request.values.get('job_id')
        job = AsyncResult(job_id, app=celery_app)

        return json.dumps(dict(
            state=job.state,
            message=job.result.get(
                'message') if job.result else '',
            current=job.result.get('current') if job.result else 0,
            total=job.result.get('total') if job.result else 10,
        ))

    @expose('/job-status')
    def job_status(self):
        job_id = request.args.get('job_id')
        return self.render('admin/job_status.html.j2', job_id=job_id)
