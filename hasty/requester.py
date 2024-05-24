import requests

from retrying import retry
from .exception import AuthenticationException, AuthorisationException, InsufficientCredits, NotFound, \
    ValidationException


def if_http_exception(exception):
    return isinstance(exception, requests.exceptions.HTTPError)


class Requester:

    def __init__(self, api_key, base_url='https://api.hasty.ai', session_id=None):
        self.api_key = api_key
        self.base_url = base_url
        self.session_id = session_id
        self.headers = {
            'accept': 'application/json',
            'X-Api-Key': self.api_key,
        }
        self.cookies = dict(ui_last_state=self.session_id)

    @retry(stop_max_attempt_number=7, wait_fixed=2000, retry_on_exception=if_http_exception)
    def request(self, method, endpoint, headers, params=None, json_data=None, data=None, files=None, cookies=None):
        url = self.base_url + endpoint
        if endpoint.startswith("http"):
            url = endpoint

        response = requests.request(method,
                                    url,
                                    headers=headers,
                                    params=params,
                                    json=json_data,
                                    cookies=cookies,
                                    data=data,
                                    files=files)
        if response.status_code == 400:
            raise ValidationException(response.json().get("message"))

        if response.status_code == 401:
            raise AuthenticationException.failed_authentication()

        if response.status_code == 402:
            raise InsufficientCredits.insufficient_credits()

        if response.status_code == 403:
            raise AuthorisationException.permission_denied()

        if response.status_code == 404:
            raise NotFound.object_not_found()

        if response.status_code > 299:
            response.raise_for_status()

        return response

    def get(self, endpoint, query_params=None):
        json_data = self.request("GET", endpoint,
                                 headers=self.headers,
                                 params=query_params,
                                 cookies=self.cookies).json()
        return json_data

    def post(self, endpoint, json_data=None, content_type='application/json', query_params=None):
        self.headers['Content-Type'] = content_type
        return self.request("POST", endpoint,
                            headers=self.headers,
                            json_data=json_data,
                            params=query_params,
                            cookies=self.cookies).json()

    def put(self, endpoint, data=None, files=None, content_type='application/json', json_data=None):
        self.headers['Content-Type'] = content_type
        response = self.request("PUT",
                                endpoint,
                                headers=self.headers,
                                data=data,
                                files=files,
                                json_data=json_data,
                                cookies=self.cookies)

        if not data:
            if response.status_code == 200:
                return response.json()
            return None

        return None, response.status_code

    def patch(self, endpoint, json_data=None, content_type='application/json'):
        self.headers['Content-Type'] = content_type
        return self.request("PATCH", endpoint,
                            headers=self.headers,
                            json_data=json_data,
                            cookies=self.cookies).json()

    def delete(self, endpoint, json_data=None):
        response = self.request("DELETE", endpoint,
                                headers=self.headers,
                                json_data=json_data,
                                cookies=self.cookies)

        if response.status_code != 204:
            # TODO Handle different status codes
            raise Exception("Something went wrong {}", response, response.text)
