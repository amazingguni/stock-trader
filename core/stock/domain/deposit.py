from datetime import datetime
from mongoengine import Document, DateTimeField, IntField


class Deposit(Document):
    deposit = IntField()
    d2_withdrawable_deposit = IntField()
    created_at = DateTimeField(default=datetime.now)
