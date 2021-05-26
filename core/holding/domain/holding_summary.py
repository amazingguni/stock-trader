from datetime import datetime

from mongoengine import Document, EmbeddedDocument, \
    StringField, DateTimeField, IntField, FloatField, EmbeddedDocumentListField


class Holding(EmbeddedDocument):
    stock_name = StringField(required=True, help_text='종목 이름')
    stock_code = StringField(required=True, help_text='종목 코드')
    quantity = IntField(help_text='보유수량')
    purchase_price = IntField(help_text='매입가')
    current_price = IntField(help_text='현재가')
    eval_profit_loss_price = IntField(help_text='평가손익')
    earning_rate = FloatField(help_text='수익률(%)')
    total_purchase_price = IntField(help_text='매입금액')


class HoldingSummary(Document):
    account_number = StringField(required=True)
    total_purchase_price = IntField(help_text='총매입금액')
    total_eval_price = IntField(help_text='총평가금액')
    total_eval_profit_loss_price = IntField(help_text='총평가손익금액')
    total_earning_rate = FloatField(help_text='총수익률(%)')
    estimated_deposit = IntField(help_text='추정예탁자산')
    holdings = EmbeddedDocumentListField(
        Holding, default=list, help_text='보유 종목별 상세 내역')
    created_at = DateTimeField(default=datetime.now)
