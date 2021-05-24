from datetime import datetime

from mongoengine import Document, \
    ReferenceField, DateTimeField, IntField, FloatField

from core.account.domain import Account


class HoldingSummary(Document):
    account = ReferenceField(Account)
    total_purchase_price = IntField(help_text='총매입금액')
    total_eval_price = IntField(help_text='총평가금액')
    total_eval_profit_loss_price = IntField(help_text='총평가손익금액')
    total_earning_rate = FloatField(help_text='총수익률(%)')
    estimated_deposit = IntField(help_text='추정예탁자산')
    created_at = DateTimeField(default=datetime.now)