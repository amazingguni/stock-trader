from datetime import datetime
from mongoengine import Document, \
    DateTimeField, DateField, StringField, IntField


class DailyStockSummary(Document):
    date = DateField(required=True)
    stock_code = StringField(required=True)
    open = IntField()
    high = IntField()
    low = IntField()
    close = IntField()
    volume = IntField()
    created_at = DateTimeField(default=datetime.now)
