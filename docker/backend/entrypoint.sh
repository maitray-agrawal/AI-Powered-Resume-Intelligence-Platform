#!/bin/sh

# Exit on error
set -e

echo "Starting backend entrypoint script..."

# This script can wait for database check or run Alembic migrations in future
# e.g., alembic upgrade head

# Exec the container command (such as uvicorn)
exec "$@"
