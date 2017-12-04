#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hmac, hashlib
from config import Config
import requests
import json
from time import time

ACCESS_KEY = Config.ZHIREN_API_ACCESS_KEY
SECRET_KEY = Config.ZHIREN_API_SECRET_KEY
ZHIRENAPI_BASE_URL = "https://zhiren.com"


def get_signature(http_method="", path="", payload_json="", tonce=""):
    str2sign = http_method.upper() + path + ACCESS_KEY + tonce + payload_json
    signature = hmac.new(SECRET_KEY, str2sign, digestmod=hashlib.sha256).hexdigest()
    return signature


def zhiren_get(url, payload=None):
    path = ZHIRENAPI_BASE_URL + url
    payload_json = json.dumps(payload) if payload else ""
    tonce = int(time()).__str__()
    sign = get_signature("GET", url, payload_json, tonce)
    return requests.get(path, params={
        "access_key": ACCESS_KEY,
        "tonce": tonce,
        "payload": payload_json
    } if payload else {
        "access_key": ACCESS_KEY,
        "tonce": tonce
    }, headers={
        "x-zhiren-signature": sign
    })
