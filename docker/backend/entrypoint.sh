#!/bin/sh

# Exit on error
set -e

echo "Starting backend entrypoint script..."

# If DATABASE_URL is set, wait for PostgreSQL to become available
if [ -n "$DATABASE_URL" ]; then
  echo "Checking database connection..."
  python -c "
import sys, time, psycopg2
db_url = '''$DATABASE_URL'''
if 'sqlite' in db_url:
    print('SQLite database detected, skipping connection check.')
    sys.exit(0)

print('Waiting for database to accept connections...')
for i in range(45):
    try:
        conn = psycopg2.connect(db_url, connect_timeout=3)
        conn.close()
        print('Database connection successful!')
        sys.exit(0)
    except Exception as e:
        print(f'Attempt {i+1}/45 failed: {e}. Retrying in 1s...')
        time.sleep(1)

print('Timeout waiting for database connection.')
sys.exit(1)
"
fi

# Run database migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Exec the container command (such as uvicorn)
exec "$@"
