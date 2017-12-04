#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .requests_helper import zhiren_get
from .employee_model import Employee


def get_user_by_id(user_id):
    rep = zhiren_get("/api/v2/employees/{0}".format(user_id))
    print rep.content
    return Employee.dict2cls(rep.json()) if rep.status_code == 200 else None


def get_user_by_mobile(user_mobile):
    rep = zhiren_get("/api/v2/employees/{0}".format(user_mobile))
    return Employee.dict2cls(rep.json()) if rep.status_code == 200 else None


def get_all_users_by_company():
    rep = zhiren_get("/api/v2/employees", {"token": ""})
    return [Employee.dict2cls(rel) for rel in rep.json()]
