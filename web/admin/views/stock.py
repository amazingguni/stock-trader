from flask_admin.actions import action
from flask_admin.contrib.mongoengine import ModelView
from flask import flash
from core.stock.domain.stock_summary import DailyStockSummary


class StockView(ModelView):
    column_searchable_list = ('name', 'code')
    column_filters = ['is_managing', 'is_insincerity', 'sector']

    @action('delete_daily_summaries', 'Delete daily summaries', 'Are you sure you want to delete all daily summaries?')
    def action_delete_daily_summaries(self, ids):
        try:
            total_count = 0
            for stock_id in ids:
                total_count += DailyStockSummary.objects(
                    stock=stock_id).count()
                DailyStockSummary.objects(stock=stock_id).delete()
            flash(f'{total_count} summary were successfully deleted.')
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(f'Failed to delete summaries. {str(ex)}', 'error')
