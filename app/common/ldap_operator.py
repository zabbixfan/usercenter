#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ldap
from .ldap_user_info import LdapUserInfo
from config import Config

ldapServer = Config.LDAP_SERVER
conn = ldap.initialize(ldapServer)

baseDN = Config.LDAP_BaseDN
user_format_string = "cn=%s,"+baseDN


def authentication(userName, password):
    """
    LDAP 用户身份验证
    :param userName:
    :param password:
    :return:
    """
    dn = user_format_string % userName
    try:
        conn.simple_bind_s(dn, password)
        return True
    except Exception,e:
        print e
        return False


def getUserInfo(userName):
    """
    获取用户信息
    :param userName:
    :return:
    """
    searchScope = ldap.SCOPE_SUBTREE
    filterstr = "cn=%s" % userName
    ldap_result_id = conn.search(baseDN, searchScope, filterstr)
    result_type, result_data = conn.result(ldap_result_id)
    if result_data.__len__() == 0:
        return None
    return LdapUserInfo(result_data[0])


def searchUserByisplayName(keyword):
    """
    根据displayName模糊搜索
    :param keyword:
    :return:
    """
    searchScope = ldap.SCOPE_SUBTREE
    filterstr = "displayName=%s*" % keyword
    try:
        ldap_result_id = conn.search(baseDN, searchScope, filterstr.encode("utf-8"))
        result_type, result_data = conn.result(ldap_result_id)
        if result_data.__len__() == 0:
            return []
        return [LdapUserInfo(data) for data in result_data]
    except Exception as e:
        print e
        return []


def searchUserByCN(keyword):
    """
    根据cn模糊搜索
    :param keyword:
    :return:
    """
    searchScope = ldap.SCOPE_SUBTREE
    filterstr = "cn=%s*" % keyword
    try:
        ldap_result_id = conn.search(baseDN, searchScope, filterstr)
        result_type, result_data = conn.result(ldap_result_id)
        if result_data.__len__() == 0:
            return []
        return [LdapUserInfo(data) for data in result_data]
    except Exception,e:
        print e
        return []