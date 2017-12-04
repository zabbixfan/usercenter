#!/usr/bin/env python
# -*- coding: utf-8 -*-
import app.common.ldap_operator as ldap
from ..models.user import User, UserStatusEnum
from config import Config
from ..common.EmailOperator import SendEmail
from itsdangerous import TimedJSONWebSignatureSerializer as JwtSerializer
from time import time


def login(login_name, pwd):
    user = None
    if Config.AUTH_PROVIDER == 'LDAP':
        user = ldap_auth_provider(login_name, pwd)
    else:
        user = default_auth_provider(login_name, pwd)
    return user


def ldap_auth_provider(login_name, pwd):
    if ldap.authentication(login_name, pwd):
        ldap_user = ldap.getUserInfo(login_name)
        return UserInfo.convert_by_ldap_user(ldap_user)
    else:
        return None


def default_auth_provider(login_name, pwd):
    user = User.authentication(login_name, pwd)
    return UserInfo.convert_by_user(user)


def get_user_by_id(user_id):
    user = None
    if Config.AUTH_PROVIDER == 'LDAP':
        user = ldap_user_provider(user_id)
    else:
        user = default_user_provider(user_id)
    return user


def ldap_user_provider(user_id):
    ldap_user = ldap.getUserInfo(user_id)
    return UserInfo.convert_by_ldap_user(ldap_user)


def default_user_provider(user_id):
    user = User.get_regular_user_by_id(user_id)
    return UserInfo.convert_by_user(user)


class UserInfo(object):
    def __init__(self, id, name, email, phone, login_name=None, empno=None, has_otp=False):
        self.phone = phone
        self.email = email
        self.name = name
        self.id = id
        self.login_name = login_name if login_name else id
        self.empno = empno if empno else ''
        self.role = ""
        self.has_otp = has_otp

    def cls2dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "phone": self.phone,
            "loginName": self.login_name,
            "empno": self.empno,
            "role": self.role,
            "hasOTP": self.has_otp
        }

    @staticmethod
    def convert_by_user(user):
        return UserInfo(user.user_id, user.user_name, user.get_mail(), user.user_mobile, user.user_login_name,
                    user.user_empno, has_otp=True if user.otp_key else False) if user else None

    @staticmethod
    def convert_by_ldap_user(ldap_user):
        return UserInfo(ldap_user.cn, ldap_user.name, ldap_user.mail, ldap_user.phone) if ldap_user else None


def forgot_password(empno, reset_pwd_url):
    user = User.get_by_empno(empno)
    if user is None or user.user_status == UserStatusEnum.dimission:
        return False, '查无此人'
    elif user.user_login_name == '' or user.get_mail() == '':
        return False, '账户未激活'
    else:
        send_reset_pwd_email(user, reset_pwd_url)
        return True, '已发送邮件至 {0}，请注意查收。'.format(user.get_mail())


def reset_password(userid, password):
    user = User.get_by_id(userid)
    if user:
        user.reset_password(password)
        return True
    return False


def change_password(userid, old_pwd, new_pwd):
    user = User.get_by_id(userid)
    if user and user.pwd_is_correct(old_pwd):
        user.reset_password(new_pwd)
        return True
    return False


def send_reset_pwd_email(user, reset_pwd_url):
    email_tmplate = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0" name="viewport" />
    <style>
    @media screen and (min-width:1px) and (max-width:739px) {
        .notice_table {
            width:96%;
            padding: 0 2%;
        }
        .notice_td{
            width: 100%
        }
    }
    </style>
</head>
<body>
<table cellpadding="0" cellspacing="0" align="center" style="background: rgb(232, 232, 232);" width="100% !important">
    <tbody>
        <tr>
            <td>
                <table height="50px"> </table>
            </td>
        </tr>
        <tr>
            <td>
                <table class="notice_table" cellpadding="0" cellspacing="0" align="center" style="text-align:left;font-family:'微软雅黑','黑体',arial;"
                    width="740">
                    <tbody>
                        <tr>
                            <td class="notice_td" style="text-align:left;color:#454545;background-color:#fff;font-size:14px;padding:0 60px;border-radius:10px"
                                width="740">
                                <table cellpadding="0" cellspacing="0" style="border-radius:10px;width: 100%">
                                    <tbody>
                                        <tr height="25">
                                            <td></td>
                                        </tr>
                                        <tr>
                                            <td style="padding-bottom:20px;font:24px '微软雅黑','黑体',arial;text-align:left; color: #cccccc"
                                                colspan="2">ALOPEX 密码重置</td>
                                        </tr>
                                        <tr>
                                            <td align="center" valign="top" height="1px" width="100%" style="background-color:#e5e5e5;line-height:1px;"
                                                colspan="2"></td>
                                        </tr>
                                        <tr height="88">
                                            <td style="vertical-align:middle;text-align:left" colspan="2"><h2>您好</h2></td>
                                        </tr>
                                        <tr>
                                            <td style="padding-bottom:20px;font:14px/24px '微软雅黑','黑体',arial;text-align:left;"
                                                colspan="2">
                                                <p style="text-align:justify;margin-bottom:0px;margin-top:20px;padding:0">
                                                     您刚刚申请重置密码，请点击 <a href="
                                                     """ + (reset_pwd_url + get_token(user)) + """
                                                ">重置密码</a> 进行密码重置。
                                                    <br><small>（为保障账号安全性，该链接仅在 3 小时内有效。如果您并不想更换密码或非你本人申请重置密码，无需进行任何操作）</small>
                                                </p>
                                            </td>
                                        </tr>

                                        <tr height="25">
                                            <td></td>
                                        </tr>
                                        <tr>
                                            <td align="center" valign="top" height="1px" width="100%" style="background-color:#e5e5e5;line-height:1px;"
                                                colspan="2"></td>
                                        </tr>
                                        <tr height="15">
                                            <td></td>
                                        </tr>
                                        <tr>
                                            <td colspan="2">
                                                <p style="font:normal 12px/24px '微软雅黑','黑体',arial;margin:0px;color:#969696;text-align:center;">
                                                    该邮件为  <a href="http://opskit.apitops.com" target="_blank" style="text-decoration:none;color:#006ec3;">Onekit</a> 系统自动发送，请勿直接回复。如有疑问，请联系运维，谢谢。
                                                </p>
                                            </td>
                                        </tr>
                                        <tr height="15">
                                            <td></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <table height="50px"> </table>
            </td>
        </tr>
    </tbody>
</table>
</body>
</html>
    """

    SendEmail([user.get_mail()], 'ALOPEX 密码重置', email_tmplate, "html", 'ALOPEX System')


def get_token(user):
    s = JwtSerializer(secret_key="I dont know", expires_in=10800)
    return s.dumps({
        "userid": user.user_id,
        "username": user.user_name,
        "loginname": user.user_login_name,
        "issued_at": time()
    })


def get_dict_by_token(token):
    try:
        s = JwtSerializer(secret_key="I dont know")
        return s.loads(token)
    except:
        return None


def login_with_otp(login_name, pwd, otp):
    user = User.authentication_with_otp(login_name, pwd, otp)
    return UserInfo(user.user_id, user.user_name, user.get_mail(), user.user_mobile, user.user_login_name,
                    user.user_empno) if user else None
