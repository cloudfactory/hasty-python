#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 09:40:28 2020

@author: kostya
"""

import requests

from . import api_base, api_key, api_session

retry_strategy = requests.packages.urllib3.util.retry.Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)


def get(endpoint, **kwargs):
    adapter = requests.adapters.HTTPAdapter()
    s = requests.Session()
    s.headers.update({'X-Api-Key': api_key})
    s.mount("https://", adapter)
    url = api_base+endpoint
    response = s.get(url, params=kwargs)
    if response.status_code == 401:
        raise ValueError('Not authorized, check API KEY')
    return response.json()


def post(endpoint, json_data=None, files=None, data=None):
    s = requests.Session()
    s.headers.update({'X-Api-Key': api_key})
    s.headers.update({"X-Session-Id": api_session})
    s.headers.update({'accept': 'application/json'})
    response = s.post(api_base+endpoint, json=json_data, files=files, data=data)
    if response.status_code == 401:
        raise ValueError('Not authorized, check API KEY')
    return response.json()


def delete(endpoint, json_data=None):
    s = requests.Session()
    s.headers.update({'X-Api-Key': api_key})
    s.headers.update({"X-Session-Id": api_session})
    s.headers.update({'accept': 'application/json'})
    response = s.delete(api_base + endpoint, json=json_data)
    if response.status_code == 401:
        raise ValueError('Not authorized, check API KEY')
    return response.json()
