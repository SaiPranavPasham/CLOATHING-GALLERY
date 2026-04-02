#!/bin/bash

echo "Starting app..."

python manage.py migrate --noinput

# Create superuser automatically
python manage.py createsuperuser \
  --noinput \
  || true

python manage.py collectstatic --noinput

gunicorn dashboard_project.wsgi --bind 0.0.0.0:$PORT