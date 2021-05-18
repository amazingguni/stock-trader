# stock-trader

[![pytest](https://github.com/amazingguni/stock-trader/actions/workflows/pytest.yml/badge.svg)](https://github.com/amazingguni/stock-trader/actions/workflows/pytest.yml) [![codecov](https://codecov.io/gh/amazingguni/stock-trader/branch/main/graph/badge.svg?token=UH56VG0M1Q)](https://codecov.io/gh/amazingguni/stock-trader)

자동 주식 거래를 위한 웹 서비스입니다. DDD(Domain Driven Design) 공부 겸 투자 목적으로 개발하고 있습니다.

## Requiremensts

- Windows
- 키움증권 OpenAPI+ ([here](https://www3.kiwoom.com/nkw.templateFrameSet.do?m=m1408010600))
- Python 3.9 32bit
- poetry ([here](https://python-poetry.org/))
- mongodb ([here](https://www.mongodb.com/cloud/atlas/lp/try2?utm_source=google&utm_campaign=gs_apac_south_korea_search_core_brand_atlas_desktop&utm_term=mongodb&utm_medium=cpc_paid_search&utm_ad=e&utm_ad_campaign_id=12212624365&gclid=Cj0KCQjw4v2EBhCtARIsACan3nxgrkJ3z2Ba1Zf4Jt7xHZErqWuGy9wp0eZ89X03ceI4OMwIouW258EaAidJEALw_wcB))
- redis ([here](https://github.com/MicrosoftArchive/redis/releases))

## Install Dependency

```sh
$ poetry install
```
## How to run

Run databases first

```sh
# Window에서 docker 메모리 사용량이 너무나도 많아서... 저는 그냥 설치형으로 사용합니다
$ docker-compose up -d
```

```sh
$ poetry run flask run
# Run selery
# window에서는 solo를 쓰지 않으면 worker가 생성되지 않는 문제가 있으니 주의 요망
$ celery -A celery_app worker -l INFO  --pool=solo
```



## How to test

```sh
$ poetry run pytest
```
