from datetime import datetime

from mongoengine import Document, \
    ReferenceField, DateTimeField, IntField, FloatField

from core.stock.domain import Stock
from core.account.domain import Account


class Holding(Document):
    account = ReferenceField(Account, help_text='보유 종목이 포함된 계좌')
    stock = ReferenceField(Stock, help_text='종목')
    quantity = IntField(help_text='보유수량')
    purchase_price = IntField(help_text='매입가')
    current_price = IntField(help_text='현재가')
    eval_profit_loss_price = IntField(help_text='평가손익')
    earning_rate = FloatField(help_text='수익률(%)')
    total_purchase_price = IntField(help_text='매입금액')

    created_at = DateTimeField(default=datetime.now)
