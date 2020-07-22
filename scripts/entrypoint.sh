#!/bin/sh

set -e

# Wait for database to boot up
echo "Collect static files"
python manage.py wait_for_db

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

uwsgi --socket :8000 --master --enable-threads --module app.wsgi

