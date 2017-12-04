#!/usr/local/flexgw/python/bin/python
# -*- coding: utf-8 -*-
"""
    openvpn-auth
    ~~~~~~~~~~~~

    openvpn account auth scripts.
"""
import os
import sys
import requests


def _auth(user_name, password):
    try:
        auth_url = "http://192.168.3.166:8000/vpn_login"
        otp = password[-6:]
        req = requests.post(auth_url, {
            "loginname": user_name,
            "password": password[:-6],
            "otp": otp
        })
        res = req.json()
        if res['isPass']:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception, e:
        sys.exit(1)

if __name__ == '__main__':
    _auth(os.environ['username'], os.environ['password'])
