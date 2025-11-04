.PHONY: start stop restart lint type-check analyze test

start:
	./start-all.sh

stop:
	./stop-all.sh

restart: stop start

lint:
	ruff check .

type-check:
	mypy --install-types --non-interactive src/ airflow/

analyze: lint type-check

test:
	pytest -v