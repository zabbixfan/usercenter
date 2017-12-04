#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask import request, g
from flask_restful import Resource, reqparse
from ..common.ApiResponse import ApiResponse, ResposeStatus
from ..common.alopex_auth_sdk import api_need_user
from ..models.user import User
from config import Config
import pyotp


def post_args():
    rp = reqparse.RequestParser()
    rp.add_argument("key", type=unicode, required=True, nullable=False)
    rp.add_argument("otp", type=unicode, required=True, nullable=False)
    return rp.parse_args()


class TOTPResource(Resource):
    def get(self):
        key = pyotp.random_base32()
        return ApiResponse({
            "key": key,
            "url": pyotp.TOTP(key).provisioning_uri(request.host, Config.OTP_NAME)
        })

    @api_need_user()
    def post(self):
        args = post_args()
        if pyotp.TOTP(args.key).verify(args.otp):
            User.set_otp_key(g.userID, args.key)
            return ApiResponse(status=ResposeStatus.Success)
        return ApiResponse(status=ResposeStatus.OTPVerifyFail)

    @api_need_user()
    def delete(self):
        User.set_otp_key(g.userID, "")
        return ApiResponse()


api.add_resource(TOTPResource, "/totp")
