from datetime import date

from core.stock.domain.repository.daily_stock_repository import DailyStockRepository
from core.stock.domain.stock import DailyStock, StockSummary


def get_dummy_daily_stock():
    return DailyStock(
        date=date(2010, 10, 2),
        stock_code='CODE',
        stock_summary=StockSummary(
            open=1,
            high=1,
            low=1,
            close=1,
            volume=1,
        )
    )


def test_save(mongo_connection):
    stock = get_dummy_daily_stock()
    # When
    DailyStockRepository().save(stock)

    assert DailyStock.objects.count() == 1


def test_save_all(mongo_connection):
    stocks = [get_dummy_daily_stock()] * 10
    # When
    DailyStockRepository().save_all(stocks)

    # Then
    assert DailyStock.objects.count() == 10


def test_find_latest_by_stock_code_GIVEN_single_stock(mongo_connection):
    repository = DailyStockRepository()
    stock = get_dummy_daily_stock()
    repository.save(stock)

    # When
    ret_stock = repository.find_latest_by_stock_code(stock.stock_code)

    # Then
    assert ret_stock == stock


def test_find_latest_by_stock_code_GIVEN_double_stock(mongo_connection):
    repository = DailyStockRepository()
    stock_a = DailyStock(
        date=date(2010, 1, 2),
        stock_code='CODE'
    )
    stock_b = DailyStock(
        date=date(2021, 3, 5),
        stock_code='CODE'
    )
    repository.save_all([stock_a, stock_b])

    # When
    ret_stock = repository.find_latest_by_stock_code(stock_a.stock_code)

    # Then
    assert ret_stock == stock_b


def test_find_latest_by_stock_code_GIVEN_different_code(mongo_connection):
    repository = DailyStockRepository()
    stock = DailyStock(
        date=date(2010, 1, 2),
        stock_code='CODE'
    )
    other_stock = DailyStock(
        date=date(2021, 3, 5),
        stock_code='OTHER_CODE'
    )
    repository.save_all([stock, other_stock])

    # When
    ret_stock = repository.find_latest_by_stock_code(stock.stock_code)

    # Then
    assert ret_stock == stock
