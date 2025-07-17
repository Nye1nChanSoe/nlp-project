import random
import time
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from .config import SLEEP_MIN, SLEEP_MAX


def get_retry_session():
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def sleep_random():
    duration = random.uniform(SLEEP_MIN, SLEEP_MAX)
    time.sleep(duration)
