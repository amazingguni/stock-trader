from datetime import datetime
from mongoengine import Document, DateTimeField, IntField, ReferenceField
from core.account.domain import Account


class Deposit(Document):
    account = ReferenceField(Account, required=True)
    deposit = IntField()
    d2_withdrawable_deposit = IntField()
    created_at = DateTimeField(default=datetime.now)
