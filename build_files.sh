#!/bin/bash

# Build script for Vercel deployment
# This runs during the Vercel build phase

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
cd myproject
python manage.py collectstatic --noinput --clear

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Build complete!"
