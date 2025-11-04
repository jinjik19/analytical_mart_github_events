#!/usr/bin/env bash

# Set AIRFLOW_UID to the current user's UID
export AIRFLOW_UID=$(id -u)

# Create Docker network if it doesn't exist
docker network create analytical_mart_network || true

echo "Starting all services..."
echo "1. Run 'Docker Compose' for DWH stack..."
docker-compose --env-file .env -f dwh_stack/docker-compose.yml --project-name github_events_platform up --build -d

echo "2. Run 'Docker Compose' for Airflow..."
docker-compose --env-file .env -f airflow/docker-compose.yml --project-name github_events_platform up --build -d

echo "All services are starting up."
