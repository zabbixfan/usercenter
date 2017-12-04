#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db
from ..models.user import User, UserStatusEnum
from ..models.department import Department
from ..common import time_helper
import re
from ..models.user_log import UserLog
from ..common import ZhiRenAPISDK

def getUsersBySystime(systime=None):
    query = db.session.query(User)
    if systime:
        query = query.filter(User.sys_time > time_helper.timestamp_to_datetime(systime))

    users = query.filter(User.user_login_name != '').all()
    return [{
        "id": user.user_id,
        "name": user.user_name,
        "loginName": user.user_login_name,
        "password": user.user_password,
        "mobile": user.user_mobile,
        "mail": user.get_mail(),
        "status": user.user_status
    } for user in users]


def searchUsersByName(keyword):
    if keyword:
        query = db.session.query(User, Department).join(Department, Department.department_id == User.department_id)
        if re.match(r'^[a-zA-Z]', keyword):
            query = query.filter(User.user_login_name.like(keyword + '%'))
        elif re.match(r'^[0-9]', keyword):
            query = query.filter(User.user_empno.like(keyword + '%'))
        else:
            query = query.filter(User.user_name.like(keyword + '%'))
        users = query.filter(User.user_status.in_([UserStatusEnum.probation, UserStatusEnum.regular])).limit(10).all()
        return [{
            "id": user.User.user_id,
            "loginName": user.User.user_login_name,
            "name": user.User.user_name,
            "department": user.Department.department_name,
        } for user in users]
    else:
        return []


def getUsersByDepartment(department_id):
    department = Department.get_by_id(department_id)
    if department:
        departments = Department.get_all_sub_list(department_id)
        departments.append(department)
        department_ids = [dep.department_id for dep in departments]
        return db.session.query(User).filter(User.department_id.in_(department_ids)).filter(
            User.user_status != UserStatusEnum.dimission).all()


def saveUser(new_user):
    log = UserLog()
    log.department_id_new = new_user.department_id
    log.user_status_new = new_user.user_status
    print new_user.department_id
    if new_user.user_id:
        if new_user.user_id:
            # 数据回滚
            db.session.expire(new_user,["department_id","user_status"])
            log.department_id_old = new_user.department_id
            log.user_status_old = new_user.user_status
            # 数据还原
            new_user.department_id = log.department_id_new
            new_user.user_status = log.user_status_new

    if log.user_status_new == log.user_status_old and log.department_id_old == log.department_id_new:
        new_user.save(auto_commit=True)
    else:
        new_user.save(auto_commit=False)
        log.user_id = new_user.user_id
        log.save_to_today(auto_commit=True)


def get_user_leader_info_by_login_name(login_name):
    current_user = User.get_user_info_by_user_login_name(login_name)
    if current_user:
        zhiren_info = ZhiRenAPISDK.get_user_by_id(current_user.zhiren_uuid)
        if zhiren_info:
            print zhiren_info.cls2dict()
            return User.get_user_by_zhiren_uuid(zhiren_info.leader_uuid)
    return None