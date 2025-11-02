# Analytical GitHub Events mart

This project builds a complete Data Lakehouse pipeline for analyzing open-source project activity on GitHub.
It covers the full data flow — from extracting large-scale GitHub Archive events and storing them in a Data Lake (MinIO), to processing with Apache Spark, loading into Greenplum, and visualizing insights through BI dashboards.

---

## 🎯 Goal

Build a fully automated data pipeline for collecting and analyzing open-source contributions in real time.

---

## ⚙️ Architecture & Tech Stack

### 🧰 Tech Stack

* [![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
* [![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E87D0E?style=for-the-badge&logo=apachespark&logoColor=white)](https://spark.apache.org/)
* [![Greenplum](https://img.shields.io/badge/Greenplum-006A44?style=for-the-badge&logo=greenplum&logoColor=white)](https://greenplum.org/)
* [![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)](https://airflow.apache.org/)
* [![Airbyte](https://img.shields.io/badge/Airbyte-615EFF?style=for-the-badge&logo=airbyte&logoColor=white)](https://airbyte.com/)
* [![Minio](https://img.shields.io/badge/Minio-C82834?style=for-the-badge&logo=minio&logoColor=white)](https://min.io/)
* [![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://www.getdbt.com/)
* [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
* [![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)
* [![Metabase](https://img.shields.io/badge/Metabase-509488?style=for-the-badge&logo=metabase&logoColor=white)](https://www.metabase.com/)
  
---

### 📊 Architecture Overview
![architecture](./docs/architecture.drawio.png)

---

## 🔧 Implementation Details

### Data Source

---

### Data Structure

---

## 🧩 Project Structure 

---

## ▶️ Getting Started

### 🧩 Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/jinjik19/analytical_mart_github_events.git
   cd analytical_mart_github_events
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   export AIRFLOW_UID=$(id -u)
   ```

3. Run the stack:
   ```bash
   docker compose -f ./infra/docker_compose/docker-compose.dev.yml -p github_events_mart up --build -d
   ```

---

## 📊 Data Model

---