#!/bin/bash
# Railway startup script for Django

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Start the application
echo "Starting Gunicorn..."
exec gunicorn Brio.wsgi --timeout 120 --limit-request-line 8190 --limit-request-field_size 8190 --worker-connections 1000

