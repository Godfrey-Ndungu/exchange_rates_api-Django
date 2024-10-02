#!/bin/bash

python manage.py migrate --settings=peachapi.production
exec gunicorn -c peachapi/gunicorn_conf.py --bind 0.0.0.0:8000 peachapi.wsgi:application --timeout 900

