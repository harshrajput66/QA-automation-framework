"""
Reusable API client for the Data QA Framework.

Encapsulates all HTTP interactions so test files don't duplicate request code.
"""
import requests
from pathlib import Path

from tests.utils.config import API_TIMEOUT


class APIClient:
    """HTTP client wrapping the Data QA API endpoints."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.timeout = API_TIMEOUT

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    def login(self, username: str, password: str):
        """POST /api/login — authenticate with credentials."""
        return self.session.post(
            f"{self.base_url}/api/login",
            json={"username": username, "password": password},
            timeout=self.timeout,
        )

    def logout(self):
        """POST /api/logout — clear the session."""
        return self.session.post(
            f"{self.base_url}/api/logout",
            headers={"Content-Type": "application/json"},
            timeout=self.timeout,
        )

    # ------------------------------------------------------------------
    # Upload
    # ------------------------------------------------------------------
    def upload_file(self, filepath: str):
        """POST /api/upload — upload a CSV file."""
        path = Path(filepath)
        with open(path, "rb") as f:
            return self.session.post(
                f"{self.base_url}/api/upload",
                files={"file": (path.name, f, "text/csv")},
                timeout=self.timeout,
            )

    def upload_file_with_name(self, filepath: str, upload_name: str):
        """POST /api/upload — upload a file with a custom filename."""
        with open(filepath, "rb") as f:
            return self.session.post(
                f"{self.base_url}/api/upload",
                files={"file": (upload_name, f)},
                timeout=self.timeout,
            )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def start_validation(self):
        """POST /api/validate — trigger the full validation pipeline."""
        return self.session.post(
            f"{self.base_url}/api/validate",
            timeout=30,  # validation can take longer
        )

    def get_status(self):
        """GET /api/status — check current validation status."""
        return self.session.get(
            f"{self.base_url}/api/status",
            timeout=self.timeout,
        )

    # ------------------------------------------------------------------
    # Results
    # ------------------------------------------------------------------
    def get_results(self):
        """GET /api/results — retrieve validation results."""
        return self.session.get(
            f"{self.base_url}/api/results",
            timeout=self.timeout,
        )

    # ------------------------------------------------------------------
    # Reports
    # ------------------------------------------------------------------
    def generate_report(self):
        """POST /api/report — generate the Excel QA report."""
        return self.session.post(
            f"{self.base_url}/api/report",
            timeout=self.timeout,
        )

    def download_report(self):
        """GET /api/report/download — download the generated report."""
        return self.session.get(
            f"{self.base_url}/api/report/download",
            timeout=self.timeout,
        )
