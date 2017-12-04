#!/usr/local/flexgw/python/bin/python
# -*- coding: utf-8 -*-
"""
    openvpn-auth
    ~~~~~~~~~~~~

    openvpn account auth scripts.
"""
import os
import re
import sys
import ldap
import logging
import logging.handlers  

LOG_FILE = 'tst.log'  
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler   

fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
formatter = logging.Formatter(fmt)   # 实例化formatter  

handler.setFormatter(formatter)      # 为handler添加formatter  

logger = logging.getLogger('tst')    # 获取名为tst的logger  
logger.addHandler(handler)           # 为logger添加handler  
logger.setLevel(logging.DEBUG)  




ldap_server = "ldap://ldap.apitops.com"
base_dn = "ou=Users,dc=tops001,dc=com"
ldap_user = "cn=admin,dc=tops001,dc=com"
ldap_password = "BwtURYTTeTN0P2m98Z"

def _validateLDAPUser(user):
  try:
    l = ldap.initialize(ldap_server)
    l.protocal_version = ldap.VERSION3
    l.simple_bind(ldap_user,ldap_password)

    searchScope = ldap.SCOPE_SUBTREE
    searchFiltername = "cn"
    retrieveAttributes = None
    searchFilter = '(' + searchFiltername + '=' + user + ')'

    ldap_result_id = l.search(base_dn,searchScope,searchFilter,retrieveAttributes)
    result_type,result_data = l.result(ldap_result_id,1)
    if(not len(result_data) == 0):
      r_a,r_b = result_data[0]
      print r_b['cn']
      return 1,r_b[u'cn'][0]
    else:
      return 0,""
  except ldap.LDAPERROR,e:
    print e
    return 0,""
  finally:
    l.unbind()
    del l

def get_dn(user,try_num = 10):
  i = 0
  isfound = 0
  foundResult= ""
  while(i < try_num ):
    isfound,foundResult = _validateLDAPUser(user)
    if(isfound):
      break
    i+=1
  print foundResult
  return foundResult

def _auth(userName,Password):
  try:
    if(Password == ""):
      print "Password Empty"
      logger.info("password empty and username is %s" % userName)  
      sys.exit(1)
    dn= get_dn(userName,10)
    if(dn == ""):
      print("not exist user")
      logger.info('not exist user username is %s' % userName)  
      sys.exit(1)
    else:
      print dn
    user_dn = "cn="+ dn + "," + base_dn
    print user_dn
    l = ldap.initialize(ldap_server)
    print l.simple_bind_s(user_dn ,Password)
    print "login ok"
    logger.info('login ok and username is %s' % userName)  
    sys.exit(0)
  except Exception,e:
    print e
    print "login failed"
    logger.info('login failed and username is %s' % userName)  
    sys.exit(1)



if __name__ == '__main__':
    _auth(os.environ['username'], os.environ['password'])
