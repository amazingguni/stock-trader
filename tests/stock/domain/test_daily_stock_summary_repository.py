from datetime import date

from core.stock.domain.repository.daily_stock_summary_repository import DailyStockSummaryRepository
from core.stock.domain.stock_summary import DailyStockSummary


def get_dummy_daily_stock_summary():
    return DailyStockSummary(
        date=date(2010, 10, 2),
        stock_code='CODE',
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


def test_find_latest_by_stock_code_GIVEN_single_stock(mongo_connection):
    repository = DailyStockSummaryRepository()
    summary = get_dummy_daily_stock_summary()
    repository.save(summary)

    # When
    ret_summary = repository.find_latest_by_stock_code(summary.stock_code)

    # Then
    assert ret_summary == summary


def test_find_latest_by_stock_code_GIVEN_double_stock(mongo_connection):
    repository = DailyStockSummaryRepository()
    summary_a = DailyStockSummary(
        date=date(2010, 1, 2),
        stock_code='CODE'
    )
    summary_b = DailyStockSummary(
        date=date(2021, 3, 5),
        stock_code='CODE'
    )
    repository.save_all([summary_a, summary_b])

    # When
    ret_summary = repository.find_latest_by_stock_code(summary_a.stock_code)

    # Then
    assert ret_summary == summary_b


def test_find_latest_by_stock_code_GIVEN_different_code(mongo_connection):
    repository = DailyStockSummaryRepository()
    summary = DailyStockSummary(
        date=date(2010, 1, 2),
        stock_code='CODE'
    )
    other_summary = DailyStockSummary(
        date=date(2021, 3, 5),
        stock_code='OTHER_CODE'
    )
    repository.save_all([summary, other_summary])

    # When
    ret_summary = repository.find_latest_by_stock_code(summary.stock_code)

    # Then
    assert ret_summary == summary
