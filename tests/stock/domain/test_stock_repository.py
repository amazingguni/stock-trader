from datetime import date

from core.stock.domain.stock import Stock, MARKET_KOSDAQ
from core.stock.domain.repository.stock_repository import StockRepository


def get_dummy_stock():
    return Stock(
        market=MARKET_KOSDAQ, name='우리회사', code='000000', sector='전자',
        major_product='반도체', listing_date=date(2018, 6, 16),
        account_month='1월', region='수지구')


def test_save_or_modify(mongo_connection):
    stock = get_dummy_stock()
    StockRepository().save_or_modify(stock)

    assert Stock.objects(code='000000').count() == 1


def test_save_or_modify_GIVEN_existing_stock(mongo_connection):
    stock = get_dummy_stock()
    StockRepository().save_or_modify(stock)

    # When
    new_stock = Stock(market=MARKET_KOSDAQ, name='우리식당', code='000000', sector='요식업',
                      major_product='양념치킨', listing_date=date(2018, 6, 16),
                      account_month='4월', region='용인')
    StockRepository().save_or_modify(new_stock)

    # Then
    assert Stock.objects(code='000000').count() == 1
    ret_stock = Stock.objects(code='000000').first()
    assert ret_stock.name == new_stock.name
    assert ret_stock.code == new_stock.code
    assert ret_stock.sector == new_stock.sector
    assert ret_stock.major_product == new_stock.major_product
    assert ret_stock.listing_date == new_stock.listing_date
    assert ret_stock.account_month == new_stock.account_month
    assert ret_stock.region == new_stock.region


def test_save_all(mongo_connection):
    stocks = []
    for i in range(1, 11):
        stocks.append(
            Stock(market=MARKET_KOSDAQ, name=f'우리식당{i}', code=f'{i:06d}', sector='요식업',
                  major_product='양념치킨', listing_date=date(2018, 6, 16),
                  account_month='4월', region='용인'))
    # When
    StockRepository().save_all(stocks)

    # Then
    assert Stock.objects.count() == 10


def test_find_all(mongo_connection):
    stocks = []
    for i in range(1, 11):
        stocks.append(
            Stock(market=MARKET_KOSDAQ, name=f'우리식당{i}', code=f'{i:06d}',
                  sector='요식업', major_product='양념치킨', listing_date=date(2018, 6, 16),
                  account_month='4월', region='용인'))
    repository = StockRepository()
    repository.save_all(stocks)

    # When
    stocks = repository.find_all()
    assert len(stocks) == 10


def test_update(mongo_connection):
    Stock(market=MARKET_KOSDAQ, name='우리식당1', code='0001').save()
    Stock(market=MARKET_KOSDAQ, name='우리식당2', code='0002').save()
    Stock(market=MARKET_KOSDAQ, name='우리식당3', code='0003').save()

    StockRepository().update_all(update={'active': False})

    assert all([s.active == False for s in Stock.objects.all()])
