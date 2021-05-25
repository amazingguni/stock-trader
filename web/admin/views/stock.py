from dependency_injector.wiring import inject, Provide
from flask import flash

from flask_admin.actions import action
from flask_admin.contrib.mongoengine import ModelView

from container import Container


class StockView(ModelView):
    column_searchable_list = ('name', 'code')
    column_filters = ['is_managing', 'is_insincerity', 'sector']

    @action('delete_daily_summaries', 'Delete daily summaries', 'Are you sure you want to delete all daily summaries?')
    @inject
    def action_delete_daily_summaries(
            self, ids,
            delete_daily_stock_summary_service=Provide[Container.delete_daily_stock_summary_service]):

        try:
            delete_daily_stock_summary_service.delete_all(ids)
            flash('summary were successfully deleted.')
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(f'Failed to delete summaries. {str(ex)}', 'error')
