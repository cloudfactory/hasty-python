#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 09:40:28 2020

@author: kostya
"""

import requests
from urllib.parse import urlencode

def get(API_class, endpoint, json_data=None):
    if json_data != None:
        query_string = f"?{urlencode(json_data)}"
    else:
        query_string = ""
    return requests.request("GET", API_class.api_base + endpoint + query_string, headers=API_class.headers).json()

def post(API_class, endpoint, json_data=None):
    return requests.request("POST", API_class.api_base + endpoint, headers=API_class.headers, json=json_data).json()

def delete(API_class, endpoint, json_data=None):
    return requests.request("DELETE", API_class.api_base + endpoint, headers=API_class.headers, json=json_data).json()