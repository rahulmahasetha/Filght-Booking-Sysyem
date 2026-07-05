#!/bin/bash

# Build script for Vercel deployment
set -e

echo "==> Current directory: $(pwd)"
echo "==> Python version: $(python3 --version)"

echo "==> Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "==> Installing Python dependencies..."
pip install -r myproject/requirements.txt

echo "==> Collecting static files..."
cd myproject
python manage.py collectstatic --noinput --clear

echo "==> Copying media files to static distribution..."
cp -r media staticfiles/media 2>/dev/null || echo "No media to copy"

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Loading fixture data into database..."
python manage.py loaddata datadump.json || echo "Data already loaded or skipping..."

echo "==> Creating admin user..."
python create_superuser.py

echo "==> Build complete!"
