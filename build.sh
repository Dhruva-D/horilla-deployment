#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Running database migrations..."
python manage.py migrate --no-input --run-syncdb

echo "Verifying migrations..."
python manage.py showmigrations

echo "Creating cache table..."
python manage.py createcachetable || true

echo "Build completed successfully!"
