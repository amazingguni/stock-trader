from datetime import datetime
from core.stock.domain.stock import Stock


def mapper(row):
    return Stock(
        name=row['회사명'],
        code='{:06d}'.format(row['종목코드']),
        sector=row['업종'],
        major_product=row['주요제품'],
        listing_date=parse_date_str(row['상장일']),
        account_month=row['결산월'],
        region=row['지역'],
    )


def parse_date_str(s: str):
    return datetime.strptime(s, '%Y-%m-%d').date()
