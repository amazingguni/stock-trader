from dependency_injector.wiring import inject, Provide

from flask_admin.contrib.mongoengine import ModelView
from flask_admin.actions import action


class StockView(ModelView):
    # column_filters = ['name']
    column_searchable_list = ('name', 'code')

    # form_ajax_refs = {
    #     'tags': {
    #         'fields': ('name',)
    #     }
    # }

    @action('crawl', 'Crawl', 'Do you want to sync stock data?')
    @inject
    def action_crawl(self, ids):
        print(ids)
