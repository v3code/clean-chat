#!/bin/sh
poetry run alembic upgrade head
poetry run uvicorn main:app --reload --host 0.0.0.0