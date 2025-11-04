
from unittest.mock import MagicMock, patch
import pytest
import requests
from tenacity import retry, stop_after_attempt, wait_none
from src.services import GArchiveClient


def test_garchive_client_download_success(mocker):
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.raw = b"test data"
    mock_session = MagicMock(spec=requests.Session)
    mock_session.get.return_value = mock_response
    mocker.patch('requests.Session', return_value=mock_session)

    client = GArchiveClient()
    result = client.download_archive("test.json.gz")

    mock_session.get.assert_called_with("https://data.gharchive.org//test.json.gz", stream=True)
    assert result == b"test data"