
class API:
    def __init__(self, api_key=None, api_base='https://api.staging.dev.hasty.ai'):
        self.api_key = api_key
        self.api_base = api_base
        self.headers = {
            'accept': 'application/json',
            'X-Api-Key': self.api_key
        }