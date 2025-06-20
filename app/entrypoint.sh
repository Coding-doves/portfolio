#!/bin/bash

echo "MySQL is up. Running migrations..."
alembic upgrade head

echo "Starting FastAPI app..."
exec uvicorn main:app --host 0.0.0.0 --port 8093 --reload