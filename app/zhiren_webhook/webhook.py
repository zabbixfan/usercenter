#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import g, request
from .zhiren_webhook_sdk_for_flask import verify_signature
from .zhiren_webhook_sdk_for_flask.employee_model import Employee as zhiren_Employee
from .zhiren_webhook_sdk_for_flask.department_model import Department as zhiren_Department
from app.models.user import User
from app.domain.user_domain import saveUser
from app.models.department import Department
from . import zhiren_webhook as app
from ..common.time_helper import strtime_to_datetime
from config import Config
from app import logger


@app.route('/webhook', methods=["POST"])
@verify_signature()
def webhook():
    logger().info(request.data)
    if g.event_type == 'department_batch_sync' or g.event_type == 'webhook_open':
        for data in getDepartmentsforLayer(g.obj_data):
            zhiren2Department(data).save()
        Department.commit()
    elif g.event_type == 'department_created' or g.event_type == 'department_updated' or g.event_type == 'department_deleted':
        zhiren2Department(g.obj_data).save()
        Department.commit()
    elif g.event_type == 'employee_created' or g.event_type == 'employee_updated' or g.event_type == 'employee_deleted':
        saveUser(zhiren2User(g.obj_data))
    return "", 200


def zhiren2Department(zdepartment):
    if zdepartment:
        current = Department.get_by_zhiren_uuid(zdepartment.uuid)
        parent = Department.get_by_zhiren_uuid(zdepartment.superior_uuid)
        rel = Department()
        if current:
            rel = current
        rel.department_name = zdepartment.name
        rel.zhiren_uuid = zdepartment.uuid
        rel.is_del = not zdepartment.disabled
        rel.parent_department = parent.department_id if parent else 0
        return rel
    else:
        return None


def getDepartmentsforLayer(departments, super=None):
    current = filter(lambda u: u.superior_uuid == super, departments)
    rel = [] + current
    for c in current:
        rel += getDepartmentsforLayer(departments, super=c.uuid)
    return rel


def zhiren2User(zEmployee):
    if zEmployee:
        current = User.get_user_by_zhiren_UUID(zEmployee.uuid)
        rel = User()
        if current:
            rel = current
        department = Department.get_by_zhiren_uuid(zEmployee.department_uuid)
        rel.department_id = department.department_id if department else 0
        rel.user_email = zEmployee.email if zEmployee.email is not None else ''
        rel.user_empno = zEmployee.empno if zEmployee.empno is not None else ''
        rel.user_exmail = zEmployee.exmail if zEmployee.exmail is not None else ''
        rel.user_job_title = zEmployee.job_title if zEmployee.job_title is not None else ''
        rel.user_join_date = strtime_to_datetime(zEmployee.join_date,
                                                 "%Y-%m-%d") if zEmployee.join_date else strtime_to_datetime(
            "1900-01-01", "%Y-%m-%d")
        rel.user_leave_date = strtime_to_datetime(zEmployee.leave_date,
                                                  "%Y-%m-%d") if zEmployee.leave_date else strtime_to_datetime(
            "1900-01-01", "%Y-%m-%d")
        rel.user_mobile = zEmployee.mobile if zEmployee.mobile is not None else ''
        rel.user_sex = zEmployee.sex if zEmployee.sex is not None else 'male'
        rel.user_status = zEmployee.status if zEmployee.status is not None else ''
        rel.user_name = zEmployee.name if zEmployee.name is not None else ''
        rel.zhiren_uuid = zEmployee.uuid if zEmployee.uuid is not None else ''
        rel.dingtalk_id = zEmployee.dingtalk_id if zEmployee.dingtalk_id is not None else ''
        rel.job_grade = zEmployee.job_grade if zEmployee.job_grade is not None else ''
        # 此处创建初始账户，不能保证账户唯一
        if not rel.user_id:
            # 用户账号密码初始化
            rel.user_login_name = rel.user_exmail.split('@')[0] if rel.user_exmail else ''
            rel.user_password = User.processPassword_md5(Config.DEFAULT_PASSWORD)
        elif not rel.user_login_name:
            # 未激活账号
            rel.user_login_name = rel.user_exmail.split('@')[0] if rel.user_exmail else rel.user_email.split('@')[
                0] if rel.user_email and rel.user_email.endswith(rel.user_empno + '@tops001.com') else ''
            rel.user_password = User.processPassword_md5(Config.DEFAULT_PASSWORD)

        return rel
    else:
        return None
