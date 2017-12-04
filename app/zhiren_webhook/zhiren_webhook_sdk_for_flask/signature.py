#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hmac, hashlib
from . import SECRET_KEY
import functools
from flask import request, abort, g
from .department_model import Department
from .employee_model import Employee


def get_string_to_sign(http_method="", path="", payload_json="", secret_key=SECRET_KEY):
    str2sign = http_method.encode().upper() + path.encode() + payload_json
    signature = hmac.new(secret_key, str2sign, digestmod=hashlib.sha256).hexdigest()
    return signature


def verify_signature(secret_key=SECRET_KEY):
    def decorator(func):
        @functools.wraps(func)
        def verify(*args, **kwargs):
            sign = get_string_to_sign(request.method, request.path, request.data, secret_key)
            if sign == request.headers.get("X-Zhiren-Signature"):
                request_json = request.json.get("event")
                event_type = request_json.get("event_type")
                live_mode = request_json.get("livemode")
                data = request_json.get("data")
                obj_data = None
                if event_type == "webhook_open":
                    # 手动开通 WebHook
                    obj_data = [Department.dict2cls(item) for item in data.get("departments")]
                elif event_type == "department_batch_sync":
                    # 手动批量同步部门信息
                    obj_data = [Department.dict2cls(item) for item in data.get("departments")]
                elif event_type == "department_created":
                    # 知人创建部门
                    obj_data = Department.dict2cls(data.get("department"))
                elif event_type == "department_updated":
                    # 知人更新部门
                    obj_data = Department.dict2cls(data.get("department"))
                elif event_type == "department_deleted":
                    # 知人删除部门
                    obj_data = Department.dict2cls(data.get("department"))
                elif event_type == "employee_created":
                    # 知人新增员工
                    obj_data = Employee.dict2cls(data.get("employee"))
                elif event_type == "employee_updated":
                    # 知人更新员工
                    obj_data = Employee.dict2cls(data.get("employee"))
                elif event_type == "employee_deleted":
                    # 知人删除员工或关闭WebHook
                    obj_data = Employee.dict2cls(data.get("employee"))

                g.obj_data = obj_data
                g.live_mode = live_mode
                g.event_type = event_type

                return func(*args, **kwargs)
            else:
                return abort(400)

        return verify

    return decorator
