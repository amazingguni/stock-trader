@Echo off
@Echo Celery Start

:repeat
@Echo Start existing celery
call poetry run celery -A celery_app worker -l INFO  --pool=solo
goto repeat
