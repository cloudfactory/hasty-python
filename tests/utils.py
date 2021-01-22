import os

from hasty import Client


def get_client():
    API_KEY = os.environ.get("HASTY_API_KEY")
    BASE_URL = os.environ.get("HASTY_BASE_URL", 'https://api.hasty.ai')
    if not API_KEY:
        raise ValueError("Environment variable HASTY_API_KEY must be set")
    h = Client(api_key=API_KEY,
               base_url=BASE_URL)
    return h
