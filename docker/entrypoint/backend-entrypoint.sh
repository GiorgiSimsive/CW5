#!/usr/bin/env bash
set -e
/app/docker/wait-for-it.sh db:5432 -t 60 -- echo "db ok"
/app/docker/wait-for-it.sh redis:6379 -t 60 -- echo "redis ok"

echo "Apply migrations"
python manage.py migrate --noinput

echo "Collect static"
python manage.py collectstatic --noinput

echo "Start gunicorn"
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2
