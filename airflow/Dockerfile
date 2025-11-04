FROM apache/airflow:3.1.0


RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock* ./
RUN uv venv .venv && \
    uv sync --no-dev