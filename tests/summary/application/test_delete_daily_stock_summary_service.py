from datetime import date

from core.stock.domain import Stock
from core.summary.domain import DailyStockSummary
from core.summary.application import DeleteDailyStockSummaryService


def create_daily_stock_summary(stock):
    return DailyStockSummary(
        date=date(2010, 10, 2),
        stock_name=stock.name,
        stock_code=stock.code,
        open=1,
        high=1,
        low=1,
        close=1,
        volume=1,
    ).save()


def test_delete_all(stock_repository, daily_stock_summary_repository):
    stock_a = Stock(name='삼성전자', code='111111',
                    market=Stock.MARKET_KOSDAQ).save()
    for _ in range(10):
        create_daily_stock_summary(stock_a)
    stock_b = Stock(name='우리은행', code='222222',
                    market=Stock.MARKET_KOSDAQ).save()
    for _ in range(8):
        create_daily_stock_summary(stock_b)
    stock_c = Stock(name='네이버', code='333333',
                    market=Stock.MARKET_KOSDAQ).save()
    for _ in range(6):
        create_daily_stock_summary(stock_c)

    DeleteDailyStockSummaryService(
        stock_repository, daily_stock_summary_repository
    ).delete_all([stock_a.id, stock_b.id])

    assert DailyStockSummary.objects(stock_code=stock_a.code).count() == 0
    assert DailyStockSummary.objects(stock_code=stock_b.code).count() == 0
    assert DailyStockSummary.objects(stock_code=stock_c.code).count() == 6
