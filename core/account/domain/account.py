from datetime import datetime
from mongoengine import Document, DateTimeField, StringField, BooleanField

SECURITIES_COMPANY_KIWOOM = '키움증권'


class Account(Document):
    primary = BooleanField(
        default=False, help_text='True인 계좌를 우선적으로 각종 명령어에 사용')
    real = BooleanField(default=True, help_text='실거래 계좌 여부(False일 경우 모의 투자 계좌')
    securities_company = StringField(help_text='증권사 이름')
    number = StringField(help_text='계좌 번호')

    created_at = DateTimeField(default=datetime.now)
