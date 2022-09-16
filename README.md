# celery_sample

simple flask app with celery

`docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management`
`docker run --name postgres -e POSTGRES_PASSWORD=example -p 5432:5432 -d postgres`

before start celery worker
`flask db upgrade`
`export FLASK_APP=app.py`

**default management creds:**

username: guest

password: guest

`celery -A celery_worker worker --loglevel=INFO --purge --pool=solo`



