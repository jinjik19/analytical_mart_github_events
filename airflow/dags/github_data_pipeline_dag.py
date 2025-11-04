import logging

import pendulum
from airflow.exceptions import AirflowSkipException
from airflow.providers.http.sensors.http import HttpSensor
from airflow.sdk import Variable, dag, task
from tenacity import RetryError

from src.services import GArchiveClient, MinioClient


logger = logging.getLogger(__name__)
access_key = Variable.get("ACCESS_KEY")
secret_key = Variable.get("SECRET_KEY")
endpoint_url = Variable.get("MINIO_ENDPOINT")
bucket_name = Variable.get("BUCKET_NAME")


@dag(
    dag_id="github_data_pipeline_dag",
    schedule="@hourly",
    start_date=pendulum.datetime(2025, 10, 3, tz="UTC"),
    catchup=False,
    tags=["github", "data_pipeline"],
)
def github_data_pipeline_dag() -> None:
    @task.short_circuit
    def check_business_hours(data_interval_start: pendulum.DateTime) -> bool:

        
        hour = data_interval_start.hour
        if 0 <= hour < 10:
            logger.warning(f"Skipping run: file for hour {hour} is not generated.")
            return False
        
        logger.info(f"Proceeding with run for hour {hour}.")
        return True

    wait_for_file = HttpSensor(
        task_id="wait_for_github_file",
        http_conn_id="github_archive_conn",
        endpoint="/{{ data_interval_start.strftime('%Y-%m-%d-%H') }}.json.gz",
        method="HEAD",
        poke_interval=60 * 5,
        timeout=60 * 60 * 3,
        mode="reschedule",
    )

    @task
    def extract_and_load_to_raw(data_interval_start: pendulum.DateTime) -> str:
        file_name = data_interval_start.strftime("%Y-%m-%d-%H") + ".json.gz"
        year = data_interval_start.year
        month = data_interval_start.month
        day = data_interval_start.day
        hour = data_interval_start.hour

        if 0 <= hour < 10:
            raise AirflowSkipException("Skipping early hour data extraction")

        garchive_client = GArchiveClient()

        try:
            raw_data_stream = garchive_client.download_archive(file_name)
        except RetryError as e:
            logger.error(f"Exceeded maximum retries to download {file_name}: {e}")
            raise e

        minio_client = MinioClient(access_key, secret_key, endpoint_url, bucket_name)
        object_key = f"raw/{year}/{month}/{day}/{file_name}"
        minio_client.upload_file(raw_data_stream, object_key)

        return object_key

    @task
    def transform_raw_to_stg(object_key: str) -> None:
        logger.info(f"Transforming raw data from {object_key} to staging area")

    @task
    def run_dbt_transformations() -> None:
        logger.info("Running dbt transformations")

    @task
    def verify_marts() -> None:
        logger.info("Verifying data marts")

    check_task = check_business_hours()

    raw_key = extract_and_load_to_raw()
    stg_task = transform_raw_to_stg(raw_key)
    dbt_task = run_dbt_transformations()

    (
        check_task
        >> wait_for_file
        >> raw_key
        >> stg_task
        >> dbt_task
        >> verify_marts()
    )


github_data_pipeline_dag()
