from mongoengine import Document, EmbeddedDocument, \
    DateTimeField, EmbeddedDocumentField, StringField, IntField


class StockSummary(EmbeddedDocument):
    open = IntField()
    high = IntField()
    low = IntField()
    close = IntField()
    volume = IntField()


class DailyStock(Document):
    date = DateTimeField()
    stock_summary = EmbeddedDocumentField(StockSummary)
