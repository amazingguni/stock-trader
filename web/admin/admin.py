from flask_admin import Admin
from core.stock.domain.stock import Stock
from core.stock.domain.stock_summary import DailyStockSummary
from .views.stock import StockView
from .views.daily_stock_summary import DailyStockSummaryView
from .views.crawl import CrawlView

admin = Admin(name='Stock Trader', url='/admin', template_mode='bootstrap4')
admin.add_view(StockView(Stock, endpoint="stock-admin"))
admin.add_view(DailyStockSummaryView(DailyStockSummary,
               endpoint="daily-stock-summary-admin"))
admin.add_view(CrawlView(name='Crawl', url='crawl'))
