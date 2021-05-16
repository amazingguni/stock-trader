from datetime import datetime
from mongoengine import Document, \
    DateTimeField, DateField, StringField


class Stock(Document):
    name = StringField(required=True, help_text='회사명')
    code = StringField(required=True, help_text='종목 코드')
    sector = StringField(help_text='업종')
    major_product = StringField(help_text='주요 제품')
    listing_date = DateField(help_text='상장일')
    account_month = StringField(help_text='결산월')
    region = StringField(help_text='지역')
    created_at = DateTimeField(default=datetime.now)
