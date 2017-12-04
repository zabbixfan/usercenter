#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ldap
from sqlalchemy import create_engine, Column, String, BigInteger, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import re
import base64, binascii, hashlib

"""
ladp 同步至 mysql 脚本
"""
LDAP_SERVER = 'LDAP://ldap.apitops.com'
LDAP_BaseDN = "ou=Users,dc=tops001,dc=com"

engine = create_engine("mysql+mysqldb://opskit:bLKGLQBtdxBVDqsk5Jy73RBkifbNML@kkinternal01.mysql.rds.aliyuncs.com/kk_opskit?charset=utf8mb4")
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
Base = declarative_base()

ADMIN_DN='cn=admin,dc=tops001,dc=com'
ADMIN_PWD='BwtURYTTeTN0P2m98Z'

ldapServer = LDAP_SERVER
conn = ldap.initialize(ldapServer)
baseDN = LDAP_BaseDN
user_format_string = "cn=%s,"+baseDN
conn.simple_bind_s(ADMIN_DN, ADMIN_PWD)

class User(Base):
    __tablename__ = 'ax_user'
    user_id = Column(String(32), primary_key=True)
    user_name = Column(String(20), default='')
    user_login_name = Column(String(255), default='')
    user_password = Column(String(255), default='')
    user_empno = Column(String(50), default='')
    user_mobile = Column(String(255), default='')
    user_email = Column(String(255), default='')
    user_exmail = Column(String(255), default='')
    user_sex = Column(String(10))
    department_id = Column(BigInteger, default=0)
    user_job_title = Column(String(255), default='')
    user_join_date = Column(TIMESTAMP)
    user_leave_date = Column(TIMESTAMP)
    user_status = Column(String(20))
    zhiren_uuid = Column(String(32), default='')

    def createAccount(self):
        re_login_name = re.compile(r'^[a-zA-Z0-9]+$')
        re_pwd = re.compile(r'^.+$')
        print re_login_name.match(self.user_login_name)
        print re_pwd.match(self.user_password)
        if self.user_login_name and self.user_password and re_login_name.match(
                self.user_login_name) is not None and re_pwd.match(self.user_password) is not None:
            if session.query(User).filter(User.user_login_name == self.user_login_name).filter(User.user_id != self.user_id).first() is None:
                session.query(User).filter(User.user_id == self.user_id).update({
                    User.user_login_name: self.user_login_name,
                    User.user_password: User.processPassword_md5(self.user_password)
                })
                session.commit()
                return True

        return False

    @staticmethod
    def processPassword_md5(pwd):
        # ldap md5 加密算法(md5->字节c缩位->base64)
        rel = '{MD5}' + base64.b64encode(binascii.unhexlify(hashlib.md5(pwd).hexdigest()))
        return rel

    @staticmethod
    def getByempno(empno):
        return session.query(User).filter(User.user_empno==empno).first()

    @staticmethod
    def getAll():
        return session.query(User).all()






def getUserInfo(empno):
    """
    获取用户信息
    :param userName:
    :return:
    """
    searchScope = ldap.SCOPE_SUBTREE
    filterstr = "sn=%s" % empno
    ldap_result_id = conn.search(baseDN, searchScope, filterstr)
    result_type, result_data = conn.result(ldap_result_id)
    if result_data.__len__() == 0:
        return None
    return result_data[0]


allUsers = User.getAll()

for user in allUsers:
    print '--------------------------------------------------------------'
    empno = user.user_empno
    print user.user_name,user.user_empno
    ldap_user = (empno)
    if ldap_user:
        login_name = ldap_user[1].get('cn')[0]
        pwd = ldap_user[1].get('userPassword')[0]
        print login_name,pwd
        user.user_login_name = login_name
        user.user_password = pwd
        print user.createAccount()

# user=User()
# user.user_id='afd40c47ece311e69648ac87a304fa2e'
# user.user_login_name='liyuanchi2202'
# user.user_password='zxc123zxc'
# print user.createAccount()