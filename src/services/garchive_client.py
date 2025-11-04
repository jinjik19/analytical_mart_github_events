import logging

import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from urllib3.response import HTTPResponse


class GArchiveClient:
    BASE_URL = "https://data.gharchive.org/"
    def __init__(self):
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

    @retry(
        wait=wait_fixed(30),
        stop=stop_after_attempt(5),
    )
    def download_archive(self, file_name: str) -> HTTPResponse:
        """Download a GArchive file by its name.
        
        Args:
            file_name (str): The name of the GArchive file to download.

        Returns:
            HTTPResponse: A stream of the downloaded file.
        """
        url = f"{self.BASE_URL}/{file_name}"
        self.logger.info(f"Downloading GArchive file from {url}")
        response = self.session.get(url, stream=True)

        if response.status_code != 200:
            self.logger.error(f"Failed to download {file_name}: {response.status_code}")
            response.raise_for_status()
        
        self.logger.info(f"Successfully downloaded {file_name}")

        return response.raw
