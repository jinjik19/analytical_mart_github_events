from unittest.mock import MagicMock
import pytest
from src.services import MinioClient


def test_minio_client_upload_success(mocker):
    mock_boto_client = MagicMock()
    mocker.patch('boto3.client', return_value=mock_boto_client)
    raw_data = b"test data stream"
    object_key = "raw/2025/10/01/test.json.gz"
    bucket_name = "test-bucket"

    client = MinioClient("fake_access", "fake_secret", "http://fake.url", bucket_name)
    client.upload_file(raw_data, object_key)

    mock_boto_client.upload_fileobj.assert_called_with(
        raw_data,
        bucket_name,
        object_key
    )
