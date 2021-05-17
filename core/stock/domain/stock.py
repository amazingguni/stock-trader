from datetime import datetime
from mongoengine import Document, \
    DateTimeField, DateField, StringField, BooleanField

MARKET_KOSPI = 'KOSPI'
MARKET_KOSDAQ = 'KOSDAQ'
MARKET_CHOICES = (MARKET_KOSPI, MARKET_KOSDAQ)


class Stock(Document):
    active = BooleanField(default=True, help_text='상장 여부')
    market = StringField(required=True, choices=MARKET_CHOICES,
                         help_text='상장된 마켓(코스피, 코스닥)')
    name = StringField(required=True, help_text='회사명')
    code = StringField(required=True, help_text='종목 코드')
    is_managing = BooleanField(default=False, help_text='관리 종목 여부')
    is_insincerity = BooleanField(default=False, help_text='불성실 공시 법인 여부')
    sector = StringField(help_text='업종')
    major_product = StringField(help_text='주요 제품')
    listing_date = DateField(help_text='상장일')
    account_month = StringField(help_text='결산월')
    region = StringField(help_text='지역')
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.name}({self.code})'
