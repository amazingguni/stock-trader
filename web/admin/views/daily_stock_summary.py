from flask_admin.contrib.mongoengine import ModelView


class DailyStockSummaryView(ModelView):
    pass

    # column_searchable_list = ('stock_code',)

    # form_ajax_refs = {
    #     'tags': {
    #         'fields': ('name',)
    #     }
    # }
