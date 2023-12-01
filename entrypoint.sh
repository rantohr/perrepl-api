#!/bin/bash

echo "Running Database Migrations..."

python /apps/manage.py migrate
python /apps/manage.py createsuperuser --brand_name tours --noinput

python /apps/manage.py runserver 0.0.0.0:8000