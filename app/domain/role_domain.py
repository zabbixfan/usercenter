#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db
from ..models.role import Role
from ..models.department import Department
from ..models.user import User
from ..models.app_client import DefaultAccessStatus


def get_list_by_appid(appid):
    rels = db.session.query(Role, User, Department).join(User, User.user_id == Role.user_id) \
        .join(Department, Department.department_id == User.department_id) \
        .filter(Role.app_id == appid).order_by(Role.role_code).all()

    return [{
        "userId": rel.User.user_id,
        "userName": rel.User.user_name,
        "department": rel.Department.department_name,
        "roleCode": rel.Role.role_code
    } for rel in rels]


def can_user_login(user_info, app_client):
    if app_client and user_info:
        # 外登录访问控制
        role = Role.get(user_info.id,app_client.app_id)
        if role:
            user_info.role = role.role_code
        if app_client.default_access_status == DefaultAccessStatus.Allow:
            return True
        elif app_client.default_access_status == DefaultAccessStatus.NotAllow:
            return True if user_info.role else False
        else:
            return False
    else:
        # 内登录访问控制
        return True

