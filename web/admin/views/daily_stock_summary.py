import mongoengine
from flask_admin.contrib.mongoengine import ModelView


class DailyStockSummaryView(ModelView):

    def scaffold_sortable_columns(self):
        columns = super(DailyStockSummaryView,
                        self).scaffold_sortable_columns()
        for n, f in self._get_model_fields():
            if isinstance(f, mongoengine.DateField):
                columns[n] = f
        return columns
