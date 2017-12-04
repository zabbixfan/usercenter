#!/usr/local/flexgw/python/bin/python
# -*- coding: utf-8 -*-
"""
    openvpn-auth
    ~~~~~~~~~~~~

    openvpn account auth scripts.
"""


import os
import re
import sys
import sqlite3
import pyotp
from flask_bcrypt import Bcrypt

DATABASE = '%s/../vpngateway/dev.db' % os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

def __validate(secret,code):
    totp = pyotp.TOTP(secret)
    code_int = int(code)
    return totp.verify(code_int)


def __query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.row_factory = sqlite3.Row
    cur = cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def _auth(name, password):
    regex = re.compile(r'^[\S\s]+$', 0)
    if not regex.match(name) or not regex.match(password) or not len(password) > 6:
        sys.exit(1)
    verify_code = password[-6:]
    verify_password =password[:-6]
    #print(verify_code)
    #print(verify_password)
    account = __query_db('select * from users where username = ?', [name], one=True)
    if account is not None:
        #print(__validate(account['otp_secret'],verify_code))
        #print(account['password'])
        bcrypt = Bcrypt()
        if bcrypt.check_password_hash(account['password'],verify_password) and __validate(account['otp_secret'],verify_code):
            print("11111")
            sys.exit(0)
        #print(bcrypt.check_password_hash(account['password'],verify_password))
    #print("2222")
    sys.exit(1)


if __name__ == '__main__':
    _auth(os.environ['username'], os.environ['password'])
