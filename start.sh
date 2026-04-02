#!/bin/sh
set -e

echo "Starting app..."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn dashboard_project.wsgi:application --bind "0.0.0.0:${PORT:-8080}"
