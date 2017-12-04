#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask_restful import Resource, reqparse
from flask import request
from ..common.ApiResponse import ApiResponse
from ..domain import account_domain


def post_args():
    rp = reqparse.RequestParser()
    rp.add_argument("empno", type=unicode, required=True, nullable=False)
    return rp.parse_args()


class ForgotPassword(Resource):
    def post(self):
        args = post_args()
        status, msg = account_domain.forgot_password(args.empno,reset_pwd_url=request.host_url+"resetpassword?usertoken=")
        return ApiResponse({
            "success": status,
            "msg": msg
        })


api.add_resource(ForgotPassword,'/forgotpassword')