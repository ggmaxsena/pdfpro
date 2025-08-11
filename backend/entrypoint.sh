#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Wait for the database to be ready
echo "Waiting for database..."
for i in $(seq 1 30); do
  if nc -z db 5432; then
    echo "Database is up!"
    break
  fi
  echo "Attempting to connect to db (attempt $i)..."
  sleep 1
done

if ! nc -z db 5432; then
  echo "Error: Database not available after 30 attempts. Aborting."
  exit 1
fi

# Apply database migrations
echo "Applying database migrations..."
poetry run python manage.py makemigrations auth_app --noinput
poetry run python manage.py migrate --noinput

# Execute the main command (passed to the script)
echo "Starting server..."
exec "$@"
