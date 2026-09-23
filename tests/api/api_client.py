import requests
from pathlib import Path

from tests.utils.config import API_TIMEOUT


class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.timeout = API_TIMEOUT

    def login(self, username, password):
        return self.session.post(
            f"{self.base_url}/api/login",
            json={"username": username, "password": password},
            timeout=self.timeout,
        )

    def logout(self):
        return self.session.post(
            f"{self.base_url}/api/logout",
            headers={"Content-Type": "application/json"},
            timeout=self.timeout,
        )

    def upload_file(self, filepath):
        path = Path(filepath)
        with open(path, "rb") as f:
            return self.session.post(
                f"{self.base_url}/api/upload",
                files={"file": (path.name, f, "text/csv")},
                timeout=self.timeout,
            )

    def upload_file_with_name(self, filepath, upload_name):
        with open(filepath, "rb") as f:
            return self.session.post(
                f"{self.base_url}/api/upload",
                files={"file": (upload_name, f)},
                timeout=self.timeout,
            )

    def start_validation(self):
        return self.session.post(
            f"{self.base_url}/api/validate",
            timeout=30,
        )

    def get_status(self):
        return self.session.get(
            f"{self.base_url}/api/status",
            timeout=self.timeout,
        )

    def get_results(self):
        return self.session.get(
            f"{self.base_url}/api/results",
            timeout=self.timeout,
        )

    def generate_report(self):
        return self.session.post(
            f"{self.base_url}/api/report",
            timeout=self.timeout,
        )

    def download_report(self):
        return self.session.get(
            f"{self.base_url}/api/report/download",
            timeout=self.timeout,
        )
