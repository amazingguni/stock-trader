from datetime import datetime

from mongoengine import Document, \
    StringField, DateTimeField, IntField, FloatField

class Holding(Document):
    account_number = StringField(required=True, help_text='보유 종목이 포함된 계좌번호')
    stock_name = StringField(required=True, help_text='종목 이름')
    stock_code = StringField(required=True, help_text='종목 코드')
    quantity = IntField(help_text='보유수량')
    purchase_price = IntField(help_text='매입가')
    current_price = IntField(help_text='현재가')
    eval_profit_loss_price = IntField(help_text='평가손익')
    earning_rate = FloatField(help_text='수익률(%)')
    total_purchase_price = IntField(help_text='매입금액')

    created_at = DateTimeField(default=datetime.now)
