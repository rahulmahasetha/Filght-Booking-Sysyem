#!/bin/bash

# Build script for Vercel deployment
set -e

echo "==> Current directory: $(pwd)"
echo "==> Python version: $(python3 --version)"
echo "==> pip version: $(pip --version 2>/dev/null || echo 'pip not found')"
echo "==> uv version: $(uv --version 2>/dev/null || echo 'uv not found')"

echo "==> Installing Python dependencies..."
# Vercel uses uv-managed Python. Try uv first, then pip with --break-system-packages
uv pip install -r myproject/requirements.txt --python python3

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
