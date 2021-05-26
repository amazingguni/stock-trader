from flask_admin import Admin
from core.account.domain import Account, Deposit
from core.stock.domain import Stock
from core.summary.domain import DailyStockSummary
from core.holding.domain import HoldingSummary

from .views.account import AccountView
from .views.deposit import DepositView
from .views.stock import StockView
from .views.daily_stock_summary import DailyStockSummaryView
from .views.holding_summary import HoldingSummaryView
from .views.sync import SyncView
# from .views.portfolio import PortfolioView

admin = Admin(name='Stock Trader', url='/admin', template_mode='bootstrap4')
# admin.add_view(PortfolioView(name='Portfolio',
#                endpoint='portfolio-admin', url='portfolio'))
admin.add_view(SyncView(name='Sync', endpoint='sync-admin', url='sync'))
admin.add_view(AccountView(Account, endpoint='account-admin'))
admin.add_view(DepositView(Deposit, endpoint='deposit-admin'))
admin.add_view(StockView(Stock, endpoint='stock-admin'))
admin.add_view(HoldingSummaryView(
    HoldingSummary, endpoint='holding-summary-admin'))
admin.add_view(DailyStockSummaryView(DailyStockSummary,
               endpoint='daily-stock-summary-admin'))
