from datetime import date

from core.summary.domain.repository import DailyStockSummaryRepository
from core.summary.domain import DailyStockSummary

from core.stock.domain import Stock


def get_dummy_daily_stock_summary():
    stock = Stock(
        market=Stock.MARKET_KOSDAQ,
        name='CODE',
        code='CODE'
    ).save()
    return DailyStockSummary(
        date=date(2010, 10, 2),
        stock_name=stock.name,
        stock_code=stock.code,
        open=1,
        high=1,
        low=1,
        close=1,
        volume=1,
    )


def test_save(mongo_connection):
    summary = get_dummy_daily_stock_summary()
    # When
    DailyStockSummaryRepository().save(summary)

    assert DailyStockSummary.objects.count() == 1


def test_save_all(mongo_connection):
    summaries = [get_dummy_daily_stock_summary()] * 10
    # When
    DailyStockSummaryRepository().save_all(summaries)

    # Then
    assert DailyStockSummary.objects.count() == 10


def test_find_latest_dates_by_stock_id(mongo_connection):
    stock_a = Stock(
        market=Stock.MARKET_KOSDAQ,
        name='A_Company',
        code='00001'
    ).save()
    stock_b = Stock(
        market=Stock.MARKET_KOSDAQ,
        name='B_Company',
        code='00002'
    ).save()
    DailyStockSummary(stock_name=stock_a.name,
                      stock_code=stock_a.code, date=date(2016, 1, 2)).save()
    DailyStockSummary(stock_name=stock_a.name,
                      stock_code=stock_a.code, date=date(2008, 1, 2)).save()
    DailyStockSummary(stock_name=stock_a.name,
                      stock_code=stock_a.code, date=date(2018, 1, 2)).save()

    DailyStockSummary(stock_name=stock_b.name,
                      stock_code=stock_b.code, date=date(2017, 1, 2)).save()
    DailyStockSummary(stock_name=stock_b.name,
                      stock_code=stock_b.code, date=date(2020, 1, 2)).save()
    DailyStockSummary(stock_name=stock_b.name,
                      stock_code=stock_b.code, date=date(2001, 1, 2)).save()

    # When
    stock_id_latest_date_dic = DailyStockSummaryRepository().find_latest_dates_by_stock_id()

    # Then
    assert stock_id_latest_date_dic
    assert stock_id_latest_date_dic[stock_a.code] == date(2018, 1, 2)
    assert stock_id_latest_date_dic[stock_b.code] == date(2020, 1, 2)


def test_delete_by_stock_code(mongo_connection):
    stock_a = Stock(
        market=Stock.MARKET_KOSDAQ,
        name='A_Company',
        code='00001'
    ).save()
    stock_b = Stock(
        market=Stock.MARKET_KOSDAQ,
        name='B_Company',
        code='00002'
    ).save()
    for _ in range(3):
        DailyStockSummary(stock_name=stock_a.name,
                          stock_code=stock_a.code, date=date(2018, 1, 2)).save()
    DailyStockSummary(stock_name=stock_b.name,
                      stock_code=stock_b.code, date=date(2017, 1, 2)).save()

    # When
    DailyStockSummaryRepository().delete_by_stock_code(stock_a.code)

    assert DailyStockSummary.objects(stock_code=stock_a.code).count() == 0
    assert DailyStockSummary.objects(stock_code=stock_b.code).count() == 1
