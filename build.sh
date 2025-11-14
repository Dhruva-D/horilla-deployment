#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Running database migrations..."
python manage.py migrate --no-input

echo "Creating cache table..."
python manage.py createcachetable || true

echo "Creating initial admin user..."
python manage.py create_initial_admin || true

echo "Build completed successfully!"
