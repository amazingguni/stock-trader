from datetime import datetime
from mongoengine import Document, EmbeddedDocument, \
    DateTimeField, DateField, EmbeddedDocumentField, StringField, IntField


class StockSummary(EmbeddedDocument):
    open = IntField()
    high = IntField()
    low = IntField()
    close = IntField()
    volume = IntField()


class DailyStock(Document):
    date = DateField(required=True)
    stock_code = StringField(required=True)
    stock_summary = EmbeddedDocumentField(StockSummary)
    created_at = DateTimeField(default=datetime.now)
