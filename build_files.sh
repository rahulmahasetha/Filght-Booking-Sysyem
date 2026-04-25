#!/bin/bash

# Build script for Vercel deployment
# This runs during the Vercel build phase

echo "==> Installing Python dependencies..."
python -m pip install -r requirements.txt --break-system-packages

echo "==> Collecting static files..."
cd myproject
python manage.py collectstatic --noinput --clear

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Seeding the database..."
python load_db.py

echo "==> Build complete!"
