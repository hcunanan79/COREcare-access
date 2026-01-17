#!/usr/bin/env bash
# Exit on error
set -o errexit

# Trigger deployment of design system consolidation (Issue #35) and MCP server integration
# Phase 3 (DOCUMENT): CSS linting to enforce design system standards

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies for CSS linting (optional, with graceful fallback)
if [ -f "package.json" ]; then
  if command -v npm &> /dev/null; then
    npm install
    # Run CSS linting (warns but doesn't fail build)
    npm run lint:css || echo "⚠️  CSS linting warnings found. See above for details."
  else
    echo "ℹ️  npm not found - skipping CSS linting. Install Node.js for design system validation."
  fi
fi

# Run database migrations (apply all pending schema changes)
python manage.py migrate

# Collect static files for production serving
python manage.py collectstatic --noinput
