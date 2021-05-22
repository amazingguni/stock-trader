from datetime import date

from core.summary.infra.kiwoom.service import DailyStockDoneCondition


def test_daily_stock_done_condition_GIVEN_same_date():
    condition = DailyStockDoneCondition(date(2020, 10, 5))
    assert condition.done({'일자': '20201005'})


def test_daily_stock_done_condition_GIVEN_before_date():
    condition = DailyStockDoneCondition(date(2020, 10, 5))
    assert condition.done({'일자': '20201003'})


def test_daily_stock_done_condition_GIVEN_after_date():
    condition = DailyStockDoneCondition(date(2020, 10, 5))
    assert not condition.done({'일자': '20201007'})
