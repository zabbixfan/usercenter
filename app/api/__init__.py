#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Api

api = Api(prefix='/api')

import user_sync, account_help, user,user_otp
