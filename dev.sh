#!/bin/bash
# Development helper script

# Make sure venv is activated
if [ -z "$VIRTUAL_ENV" ]; then
  echo "Please activate your virtual environment first"
  echo "source venv/bin/activate"
  exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
  echo "Creating .env file from template..."
  cp .env.example .env
  echo "Please edit .env file with your configuration"
fi

# Initialize database if needed
if [ ! -f instance/app.db ]; then
  echo "Initializing database..."
  python -m flask db upgrade
  echo "Creating test user..."
  python -m flask create-test-user
fi

# Run the application
echo "Starting Flask development server..."
python run.py 