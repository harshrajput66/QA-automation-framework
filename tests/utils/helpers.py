"""
Shared utility/helper functions for the test suite.
"""
import time
from pathlib import Path


def wait_for_file(file_path, timeout=10):
    """Wait for a file to exist on disk, polling every 0.5s."""
    path = Path(file_path)
    elapsed = 0
    while elapsed < timeout:
        if path.exists() and path.stat().st_size > 0:
            return True
        time.sleep(0.5)
        elapsed += 0.5
    return False


def file_size_kb(file_path):
    """Return the file size in KB."""
    path = Path(file_path)
    if path.exists():
        return round(path.stat().st_size / 1024, 2)
    return 0
