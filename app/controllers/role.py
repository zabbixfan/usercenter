#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, g, request, abort, redirect, jsonify

from . import ctl as app
from ..common import alopex_auth_sdk
from ..models.role import Role
from ..domain.role_domain import get_list_by_appid


@app.route("/app/rolemanage/<appid>", methods=["GET"])
@alopex_auth_sdk.need_login()
def get_role_list(appid):
    role_list = get_list_by_appid(appid)
    return render_template("role_list.html", user=g.user, appid=appid, roleList=role_list)


@app.route("/app/rolemanage/<appid>", methods=["POST"])
@alopex_auth_sdk.need_login()
def add_role(appid):
    users = request.form.getlist("users[]")
    role = request.form.get("role")
    Role.batchAdd(users, appid, role.strip())
    return jsonify({
        "message": "success"
    })


@app.route("/app/rolemanage/<appid>/<user>", methods=["POST"])
@alopex_auth_sdk.need_login()
def delete_role(appid, user):
    Role.delete(user,appid)
    return jsonify({
        "message": "success"
    })
