#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python myproject/manage.py collectstatic --noinput
