from datetime import date

from core.stock.infra.krx.utils import HolidayCrawler, get_last_market_opening_day


def test_crawl():
    holidays = HolidayCrawler().crawl(2021)

    assert holidays
    assert date(2021, 1, 1) in holidays


def test_get_last_market_opening_day1():
    # 석가 탄신일
    opening_day = get_last_market_opening_day(date(2021, 5, 19))

    assert opening_day == date(2021, 5, 18)
