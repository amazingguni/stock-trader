@Echo off
@Echo Start celery batch script

:repeat
@Echo Start celery again
call poetry run celery -A celery_app worker -l INFO  --pool=solo
goto repeat
