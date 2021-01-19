import requests


class Requester:

    def __init__(self, api_key, base_url='https://api.hasty.ai', session_id=None):
        self.api_key = api_key
        self.base_url = base_url
        self.session_id = session_id
        self.headers = {
            'accept': 'application/json',
            'X-Api-Key': self.api_key,
            'X-Session-Id': self.session_id
        }

    def get(self, endpoint, query_params):
        response = requests.request("GET",
                                    self.base_url + endpoint,
                                    headers=self.headers,
                                    params=query_params).json()
        return response

    def post(self, endpoint, content_type='application/json', json_data=None):
        self.headers['Content-Type'] = content_type
        return requests.request("POST",
                                self.base_url + endpoint,
                                headers=self.headers,
                                json=json_data).json()

    def put(self, endpoint, data=None, files=None, content_type='application/json', json_data=None):
        self.headers['Content-Type'] = content_type
        url = self.base_url + endpoint
        if endpoint.startswith("http"):
            url = endpoint
        response = requests.request("PUT",
                                    url,
                                    headers=self.headers,
                                    data=data,
                                    files=files,
                                    json=json_data)
        if not data:
            return response.json(), response.status_code
        return None, response.status_code

    def delete(self, endpoint):
        print(self.base_url + endpoint)
        response = requests.request("DELETE", self.base_url + endpoint)
        if response.status_code != '204':
            # TODO Handle different status codes
            raise Exception("Something went wrong", response)
