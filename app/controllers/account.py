#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, make_response, g, jsonify

from . import ctl as app
from ..common import alopex_auth_sdk
from ..domain import account_domain
from ..models.user import User

@app.route("/current/info", methods=["GET"])
@alopex_auth_sdk.need_login()
def currentUserInfo():
    user = User.get_user_info_by_user_id(g.userID)
    return render_template('current_user_info.html', user=g.user, user_info=user)


@app.route("/current/changepwd", methods=["POST"])
@alopex_auth_sdk.need_login()
def changePassword():
    oldpwd = request.form.get("oldpwd")
    newpwd = request.form.get("newpwd")
    rel = account_domain.change_password(g.userID, oldpwd, newpwd)
    return jsonify({
        "success": rel,
        "msg": "密码修改成功" if rel else "原密码验证错误"
    })


@app.route("/resetpassword", methods=["GET"])
def reset_password_view():
    token = request.args.get("usertoken")
    user_dict = account_domain.get_dict_by_token(token)
    if user_dict:
        return render_template("reset_password.html", user=user_dict, token=token)
    else:
        return render_template("error.html",msg="链接已过期")



@app.route("/resetpassword", methods=["POST"])
def reset_password():
    token = request.form.get("token")
    newpwd = request.form.get("newpwd")
    user_dict = account_domain.get_dict_by_token(token)
    if user_dict and newpwd:
        account_domain.reset_password(user_dict.get("userid"), newpwd)
        return redirect("/")
    else:
        return render_template("error.html", msg="链接已过期")

