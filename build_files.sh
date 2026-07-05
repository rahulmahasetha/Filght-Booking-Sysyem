#!/bin/bash

# Build script for Vercel deployment
set -e

echo "==> Current directory: $(pwd)"
echo "==> Python version: $(python3 --version)"

echo "==> Installing Python dependencies..."
# Vercel uses uv-managed Python — use uv pip if available, else fall back
if command -v uv &> /dev/null; then
    uv pip install -r myproject/requirements.txt --system
else
    pip install -r myproject/requirements.txt --break-system-packages
fi

echo "==> Collecting static files..."
cd myproject
python manage.py collectstatic --noinput --clear

echo "==> Copying media files to static distribution..."
cp -r media staticfiles/media 2>/dev/null || echo "No media to copy"

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Creating admin user..."
python create_superuser.py

echo "==> Build complete!"
