#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itsdangerous import TimedJSONWebSignatureSerializer as JwtSerializer
from config import Config
from time import time


class AccessTokenModel(object):
    def __init__(self, client_id, user):
        self.client_id = client_id
        self.user = user

    def cls2token(self, client_secret, exprires=Config.ACCESS_TOKEN_DEFAULT_EXPIRES):
        s = JwtSerializer(secret_key=client_secret, expires_in=exprires)
        return s.dumps({
            "client_id": self.client_id,
            "user": self.user,
            "issued_at": time()
        })

    @classmethod
    def token2cls(cls, client_secret, token):
        s = JwtSerializer(client_secret)
        try:
            data = s.loads(token)
            if "client_id" in data and "user" in data:
                return cls(data["client_id"],data["user"])
            else:
                return None
        except:
            return None


