#!/bin/bash
set -e

# Wait for database to be available
echo "Initializing application..."

# Apply database migrations
echo "Applying database migrations..."
python -m flask db upgrade

# Create test user if it doesn't exist
echo "Creating test user if needed..."
python -m flask create-test-user

# Start the application
echo "Starting application..."
exec gunicorn --bind 0.0.0.0:5000 --access-logfile - --error-logfile - run:app 