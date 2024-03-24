#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn lameli_2.wsgi:application --bind 0.0.0.0:"${BACKEND_PORT}"

