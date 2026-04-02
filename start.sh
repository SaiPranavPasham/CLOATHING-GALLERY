#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn dashboard_project.wsgi:application --bind 0.0.0.0:${PORT:-8000}
