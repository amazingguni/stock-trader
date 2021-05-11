from flask_admin import Admin
from core.stock.domain.stock import Stock
from .views.stock import StockView

admin = Admin(name='Stock Trader', url='/admin')
admin.add_view(StockView(Stock))
