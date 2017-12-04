#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask_restful import Resource, reqparse
from ..common.ApiResponse import ApiResponse
from ..domain import user_domain, account_domain


def get_args():
    rp = reqparse.RequestParser()
    rp.add_argument("starttime", type=int)
    return rp.parse_args()


def post_args():
    rp = reqparse.RequestParser()
    rp.add_argument("loginName", type=unicode, required=True, nullable=False)
    rp.add_argument("password", type=unicode, required=True, nullable=False)
    return rp.parse_args()


def post_args():
    rp = reqparse.RequestParser()
    rp.add_argument("loginName", type=unicode, required=True, nullable=False)
    rp.add_argument("password", type=unicode, required=True, nullable=False)
    rp.add_argument("otp", type=unicode, required=True, nullable=False)
    return rp.parse_args()


class UserSync(Resource):
    def get(self):
        # 用户信息同步
        args = get_args()
        return ApiResponse(user_domain.getUsersBySystime(args.starttime))


class UserVerifyPassword(Resource):
    def post(self):
        args = post_args()
        user = account_domain.login(args.loginName, args.password)
        return ApiResponse({
            "isPass": user is not None
        })


class UserVerifyPasswordWithOTP(Resource):
    def post(self):
        args = post_args()
        user = account_domain.login_with_otp(args.loginName, args.password, args.otp)
        return ApiResponse({
            "isPass": user is not None
        })


api.add_resource(UserSync, '/usersync')
api.add_resource(UserVerifyPassword, '/verifypassword')
api.add_resource(UserVerifyPasswordWithOTP, '/verifypasswordwithotp')
