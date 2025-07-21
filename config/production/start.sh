#!/bin/sh

# Start celery worker
celery -A app.celery worker --loglevel=info &

# Start celery redbeat
celery -A app.celery beat -S redbeat.RedBeatScheduler --loglevel=info &

# Start flower
celery -A app.celery flower --conf=config/flowerconfig.py &

# Start server
gunicorn --workers 10 --bind 0.0.0.0:8002 wsgi:app
