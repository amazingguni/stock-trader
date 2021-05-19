from datetime import date

from core.stock.infra.krx.utils import HolidayCrawler, get_last_market_opening_day


def test_crawl():
    holidays = HolidayCrawler().crawl(2021)

    assert holidays
    assert date(2021, 1, 1) in holidays


def test_get_last_market_opening_day_GIVEN_holiday():
    # 석가 탄신일
    opening_day = get_last_market_opening_day(date(2021, 5, 19))

    assert opening_day == date(2021, 5, 18)


def test_get_last_market_opening_day_GIVEN_saturday():
    # 토요일
    opening_day = get_last_market_opening_day(date(2021, 5, 15))

    assert opening_day == date(2021, 5, 14)


def test_get_last_market_opening_day_GIVEN_sunday():
    # 일요일
    opening_day = get_last_market_opening_day(date(2021, 5, 16))

    assert opening_day == date(2021, 5, 14)
