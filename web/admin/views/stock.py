from flask_admin.contrib.mongoengine import ModelView


class StockView(ModelView):
    # column_filters = ['name']
    column_searchable_list = ('name', 'code')

    # form_ajax_refs = {
    #     'tags': {
    #         'fields': ('name',)
    #     }
    # }
