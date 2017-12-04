#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Department(object):
    def __init__(self, name, uuid, superior_uuid, disabled=True):
        self.name = name
        self.uuid = uuid
        self.superior_uuid = superior_uuid
        self.disabled = disabled

    @classmethod
    def dict2cls(cls, data_dict):
        return cls(data_dict.get("name"), data_dict.get("uuid"), data_dict.get("superior_uuid"), data_dict.get("disabled", True))

    def cls2dict(self):
        return {
            "name": self.name,
            "uuid": self.uuid,
            "superior_uuid": self.superior_uuid,
            "disabled": self.disabled
        }
