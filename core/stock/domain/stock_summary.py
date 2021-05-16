from datetime import datetime
from mongoengine import Document, \
    DateTimeField, DateField, StringField, IntField, ReferenceField

from core.stock.domain.stock import Stock


class DailyStockSummary(Document):
    date = DateField(required=True)
    stock = ReferenceField(Stock)
    open = IntField()
    high = IntField()
    low = IntField()
    close = IntField()
    volume = IntField()
    created_at = DateTimeField(default=datetime.now)
