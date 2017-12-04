#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import binascii
import hashlib
import re
from uuid import uuid1 as uuid
import pyotp

from sqlalchemy import func, or_

from app import db
from ..common.time_helper import timestamp_to_datetime


class UserSexEnum(object):
    # 男
    male = 'male'
    # 女
    female = 'female'


class UserStatusEnum(object):
    # 在职
    regular = 'regular'
    # 离职
    dimission = 'dimission'
    # 试用
    probation = 'probation'


class User(db.Model):
    __tablename__ = "ax_user"

    user_id = db.Column(db.String(32), primary_key=True)
    user_name = db.Column(db.String(20), default='')
    user_login_name = db.Column(db.String(255), default='')
    user_password = db.Column(db.String(255), default='')
    user_empno = db.Column(db.String(50), default='')
    user_mobile = db.Column(db.String(255), default='')
    user_email = db.Column(db.String(255), default='')
    user_exmail = db.Column(db.String(255), default='')
    user_sex = db.Column(db.String(10), default=UserSexEnum.male)
    department_id = db.Column(db.BigInteger, default=0)
    user_job_title = db.Column(db.String(255), default='')
    user_join_date = db.Column(db.TIMESTAMP, default=timestamp_to_datetime(0))
    user_leave_date = db.Column(db.TIMESTAMP, default=timestamp_to_datetime(0))
    user_status = db.Column(db.String(20), default=UserStatusEnum.regular)
    zhiren_uuid = db.Column(db.String(32), default='')
    otp_key = db.Column(db.String(50), default="")
    dingtalk_id = db.Column(db.String(64), default="")
    job_grade = db.Column(db.String(50), default="")
    sys_time = db.Column(db.TIMESTAMP, server_default=func.now())

    @classmethod
    def get_user_by_zhiren_UUID(cls, uuid):
        if uuid:
            return db.session.query(cls).filter(cls.zhiren_uuid == uuid).first()
        else:
            return None

    def save(self, auto_commit=True):
        if self.user_id is None or self.user_id == "":
            self.user_id = uuid().get_hex()

        db.session.add(self)
        if auto_commit:
            db.session.commit()

    @classmethod
    def authentication(cls, login_name, pwd):
        user = db.session.query(cls) \
            .filter(cls.user_login_name == login_name) \
            .filter(or_(cls.user_status == UserStatusEnum.regular, cls.user_status == UserStatusEnum.probation)).first()

        return user if user and user.pwd_is_correct(pwd) else None

    @classmethod
    def authentication_with_otp(cls, login_name, pwd, otp):
        user = db.session.query(cls) \
            .filter(cls.user_login_name == login_name) \
            .filter(or_(cls.user_status == UserStatusEnum.regular, cls.user_status == UserStatusEnum.probation)).first()

        return user if user and user.otp_verify(otp) and user.pwd_is_correct(pwd) else None

    def otp_verify(self, otp):
        if self.otp_key and pyotp.TOTP(self.otp_key).verify(otp):
            return True
        return False

    @classmethod
    def get_regular_user_by_id(cls, user_id):
        return db.session.query(cls) \
            .filter(cls.user_id == user_id) \
            .filter(or_(cls.user_status == UserStatusEnum.regular, cls.user_status == UserStatusEnum.probation)).first()

    @staticmethod
    def processPassword_md5(pwd):
        # ldap md5 加密算法(md5->字节缩位->base64)
        rel = '{MD5}' + base64.b64encode(binascii.unhexlify(hashlib.md5(pwd).hexdigest()))
        return rel

    def pwd_is_correct(self, pwd):
        if self.user_password.startswith('{MD5}'):
            return User.processPassword_md5(pwd) == self.user_password
        else:
            return self.user_password == pwd

    def createAccount(self):
        re_login_name = re.compile(r'^.+$')
        re_pwd = re.compile(r'^.+$')
        if self.user_login_name and self.user_password and re_login_name.match(
                self.user_login_name) is not None and re_pwd.match(self.user_password) is not None:
            if db.session.query(User).filter(User.user_login_name == self.user_login_name).filter(
                            User.user_id != self.user_id).first() is None:
                db.session.query(User).filter(User.user_id == self.user_id).update({
                    User.user_login_name: self.user_login_name,
                    User.user_password: User.processPassword_md5(self.user_password)
                })
                db.session.commit()
                return True

        return False

    def get_mail(self):
        return self.user_exmail if self.user_exmail else self.user_email

    @classmethod
    def get_by_empno(cls, empno):
        return db.session.query(cls).filter(cls.user_empno == empno).first()

    def reset_password(self, password):
        db.session.query(User).filter(User.user_id == self.user_id).update({
            User.user_password: User.processPassword_md5(password)
        })
        db.session.commit()

    @classmethod
    def get_by_id(cls, userid):
        return db.session.query(cls).filter(cls.user_id == userid).first()

    @classmethod
    def set_otp_key(cls, user_id, key):
        db.session.query(cls).filter(cls.user_id == user_id).update({
            cls.otp_key: key
        })
        db.session.commit()

    @classmethod
    def get_user_info_by_user_id(cls, user_id):
        return db.session.query(cls).filter(cls.user_id == user_id).first()

    @classmethod
    def get_user_info_by_user_login_name(cls, login_name):
        return db.session.query(cls).filter(cls.user_login_name == login_name).first()

    @staticmethod
    def get_user_by_zhiren_uuid(zhiren_uuid):
        return db.session.query(User).filter(User.zhiren_uuid == zhiren_uuid).first()
