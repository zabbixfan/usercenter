#!/usr/bin/env python
# -*- coding: utf-8 -*-
class LdapUserInfo(object):
    def __init__(self,ladp_result):
        self.cn=ladp_result[1]['cn'][0]
        self.name=ladp_result[1]['displayName'][0]
        self.phone=ladp_result[1]['mobile'][0]
        self.mail=ladp_result[1]['mail'][0]

    def obj2dict(self):
        return {
            "cn":self.cn,
            "name":self.name,
            "mail":self.mail,
            "phone":self.phone
        }