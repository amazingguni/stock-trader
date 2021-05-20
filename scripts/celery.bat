@Echo off
@Echo Celery Start

:repeat
@Echo Start existing celery
CHDIR /D C:\Users\tyzm1\Documents\GitHub\stock-trader
call poetry run celery -A celery_app worker -l INFO  --pool=solo
goto repeat
