#!/usr/bin/env bash
# Exit on error
set -o errexit

# Trigger deployment of design system consolidation (Issue #35) and MCP server integration

# Install dependencies
pip install -r requirements.txt

# Run database migrations (apply all pending schema changes)
python manage.py migrate

# Collect static files for production serving
python manage.py collectstatic --noinput
