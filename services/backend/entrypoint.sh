#!/bin/sh

if [ "$DATABASE" = "admin" ]
then
    echo "Waiting for postgres..."

    while ! nc -z db 5432; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
python manage.py import-data
uvicorn main:app --reload --host=0.0.0.0 --port=8000

exec "$@"