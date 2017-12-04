#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itsdangerous import TimedJSONWebSignatureSerializer as JwtSerializer
from config import Config
from time import time


class IDTokenModel(object):
    def __init__(self, user_id):
        self.user_id = user_id

    def cls2Token(self, expires=Config.ID_TOKEN_DEFAULT_EXPIRES):
        s = JwtSerializer(secret_key=Config.ID_TOKEN_SECRET_KEY,
                          salt=Config.ID_TOKEN_SALT,
                          expires_in=expires)
        return s.dumps({
            "user_id": self.user_id,
            "issued_at": time()
        })

    @classmethod
    def token2cls(cls, token):
        if token:
            s = JwtSerializer(secret_key=Config.ID_TOKEN_SECRET_KEY, salt=Config.ID_TOKEN_SALT)
            try:
                data = s.loads(token)
                if data.get("user_id"):
                    return cls(data.get("user_id"))
                return None
            except:
                return None
        else:
            return None
