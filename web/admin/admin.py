from flask_admin import Admin
from core.stock.domain.stock import Stock
from .views.stock import StockView
from .views.crawl import CrawlView

admin = Admin(name='Stock Trader', url='/admin', template_mode='bootstrap4')
admin.add_view(StockView(Stock))
admin.add_view(CrawlView(name='Crawl', url='crawl'))
