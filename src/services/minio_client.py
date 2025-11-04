import logging

import boto3
from urllib3 import HTTPResponse


class MinioClient:
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str) -> None:
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.bucket_name = bucket_name
        self.logger = logging.getLogger(__name__)

    def upload_file(self, raw_data: HTTPResponse, object_key: str) -> None:
        """Upload a file to MinIO by its object key.

        Args:
            raw_data (HTTPResponse): The raw data stream to upload.
            object_key (str): The object key where the file will be stored.
        """
        try:
            self.client.upload_fileobj(raw_data, self.bucket_name, object_key)
            self.logger.info(f"Successfully uploaded data to MinIO with key: {object_key}")
        except boto3.exceptions.Boto3Error as e:
            self.logger.error(f"Failed to upload data to MinIO: {e}")
            raise e
