#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask_restful import Resource, reqparse
from ..common.ApiResponse import ApiResponse, ResposeStatus
from ..domain import user_domain
from ..models.user import User
from ..domain.account_domain import UserInfo


def get_args():
    rp = reqparse.RequestParser()
    rp.add_argument("keyword", type=unicode)
    return rp.parse_args()


class SearchUserResource(Resource):
    def get(self):
        args = get_args()
        rel = user_domain.searchUsersByName(args.keyword)
        return ApiResponse({
            "searchData": rel
        })


class UserInfoResource(Resource):
    def get(self, userId):
        user = User.get_user_info_by_user_id(userId)
        return ApiResponse(
            UserInfo.convert_by_user(user).cls2dict()) if user else ApiResponse()


class UserInfoCNResource(Resource):
    def get(self, cn):
        user = User.get_user_info_by_user_login_name(cn)
        return ApiResponse(UserInfo.convert_by_user(user).cls2dict()) if user else ApiResponse(status=ResposeStatus.NotFound)


class UsersByDepartmentResource(Resource):
    def get(self,department):
        rel = user_domain.getUsersByDepartment(department)
        return [
            UserInfo.convert_by_user(user).cls2dict()
         for user in rel]


class UserLeaderResource(Resource):
    def get(self,login_name):
        rel = user_domain.get_user_leader_info_by_login_name(login_name)
        return ApiResponse(UserInfo.convert_by_user(rel).cls2dict()) if rel else ApiResponse(status=ResposeStatus.NotFound)


api.add_resource(SearchUserResource, "/usersearch")
api.add_resource(UserInfoResource, "/userinfo/<userId>")
api.add_resource(UserInfoCNResource, "/userinfobycn/<cn>")
api.add_resource(UsersByDepartmentResource, "/userinfobydepartment/<department>")
api.add_resource(UserLeaderResource, "/userinfo_ln/<login_name>/leader")