from datetime import date

from core.stock.infra.kiwoom.daily_stock_done_condition import DailyStockDoneCondition


def test_daily_stock_done_condition_GIVEN_same_date():
    condition = DailyStockDoneCondition(date(2020, 10, 5))
    assert condition.done({'date': '20201005'})


def test_daily_stock_done_condition_GIVEN_before_date():
    condition = DailyStockDoneCondition(date(2020, 10, 5))
    assert condition.done({'date': '20201003'})


def test_daily_stock_done_condition_GIVEN_after_date():
    condition = DailyStockDoneCondition(date(2020, 10, 5))
    assert not condition.done({'date': '20201007'})
