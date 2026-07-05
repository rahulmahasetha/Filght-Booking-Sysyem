#!/bin/bash

# Build script for Vercel deployment
set -e

echo "==> Current directory: $(pwd)"
echo "==> Python version: $(python3 --version)"
echo "==> pip version: $(pip --version 2>/dev/null || echo 'pip not found')"
echo "==> uv version: $(uv --version 2>/dev/null || echo 'uv not found')"

echo "==> Installing Python dependencies..."
if command -v uv >/dev/null 2>&1; then
  uv pip install -r myproject/requirements.txt --system
elif command -v python3 >/dev/null 2>&1; then
  python3 -m pip install --user --disable-pip-version-check -r myproject/requirements.txt
else
  echo "No supported Python package installer is available."
  exit 1
fi

echo "==> Collecting static files..."
cd myproject
python3 manage.py collectstatic --noinput --clear

echo "==> Copying media files to static distribution..."
cp -r media staticfiles/media 2>/dev/null || echo "No media to copy"

echo "==> Running database migrations..."
python3 manage.py migrate --noinput

echo "==> Creating admin user..."
python3 create_superuser.py

echo "==> Build complete!"
