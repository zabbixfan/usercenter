#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
ctl = Blueprint('ctl', __name__,template_folder='templates',static_folder="static",static_url_path='/app/controllers/static')

import index,login,error,app_client,account,role,login_msg,mns