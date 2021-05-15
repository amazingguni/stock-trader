from flask_admin import BaseView, expose


class CrawlView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/crawl.html.j2')
