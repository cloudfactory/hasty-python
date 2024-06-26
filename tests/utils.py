import os

from hasty import Client


img_url = "https://images.ctfassets.net/hiiv1w4761fl/6NhZFymLPiX8abIUuEYV7i/c7a63c3a56e7e4f40cfd459c01a10853" \
          "/Untitled_presentation__6_.jpg?w=945&h=494&q=50&fit=fill"

vid_url = "https://storage.googleapis.com/hasty-test-fixtures/videos/WeAreGoingOnBullrun.mp4"


def get_client():
    API_KEY = os.environ.get("HASTY_API_KEY")
    BASE_URL = os.environ.get("HASTY_BASE_URL", 'https://api.hasty.ai')
    if not API_KEY:
        raise ValueError("Environment variable HASTY_API_KEY must be set")

    return Client(api_key=API_KEY, base_url=BASE_URL)
