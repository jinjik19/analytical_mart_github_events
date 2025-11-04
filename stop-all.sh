#!/bin/bash
echo "--- 🛑 Shut down project ---"

echo "--- 1. Shut down Airflow ---"
docker-compose -f airflow/docker-compose.yml --project-name github_events_platform down -v

echo "--- 2. Shut Down Data Stack (MinIO, Greenplum) ---"
docker-compose -f data-stack/docker-compose.yml --project-name github_events_platform down -v

echo "--- 3. Remove docker network ---"
docker network rm analytical_mart_network || true

echo "--- ✅ Project stopped. ---"