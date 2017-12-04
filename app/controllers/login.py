#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, make_response
import urllib
import datetime

from . import ctl as app
from ..models.id_token_model import IDTokenModel
from ..models.app_client import AppClient, AppStatus
import app.domain.account_domain as account
from ..common.common import urlAddParam
from config import Config
from ..models.access_token_model import AccessTokenModel
from ..domain.role_domain import can_user_login


@app.route("/login", methods=["GET"])
def login():
    appid = request.args.get("appid")
    callback_url = request.args.get("callback")
    callback_domain = urllib.splithost(urllib.splittype(callback_url if callback_url else "")[1])[0]
    id_token = request.cookies.get("idtoken")
    appsecret = Config.APP_SECRET
    app_client = None
    if appid:
        # 外登录
        app_client = AppClient.get_by_app_id(appid)
        if app_client:
            # app id 验证成功
            appsecret = app_client.app_secret

            if not (
                        callback_url and (
                            callback_domain == app_client.app_domain or app_client.app_status == AppStatus.Beta)):
                callback_url = app_client.app_index_url
        else:
            # app id 验证失败
            return render_template('error.html', msg="AppId 验证失败")
    else:
        # 内登录
        if not (callback_url and callback_domain == request.host):
            callback_url = "http://{0}/".format(request.host)

    if id_token:
        id_token_obj = IDTokenModel.token2cls(id_token)
        if id_token_obj:
            user = account.get_user_by_id(id_token_obj.user_id)
            if user:
                if can_user_login(user, app_client):
                    access_token = AccessTokenModel(appid, user=user.cls2dict()).cls2token(appsecret)
                    return redirect(urlAddParam(callback_url, accesstoken=access_token))
                else:
                    return render_template('error.html', msg="没有权限访问")
    # 未登录或登录失效
    return render_template('login.html', callback_url=callback_url, appid=appid)


@app.route("/login", methods=["POST"])
def authorize():
    appid = request.form.get("appid")
    callback_url = request.args.get("callback")
    login_name = request.form.get("name")
    pwd = request.form.get("pwd")
    keeplogin = request.form.get("keeplogin")
    callback_domain = urllib.splithost(urllib.splittype(callback_url if callback_url else "")[1])[0]
    appsecret = Config.APP_SECRET
    app_client = None
    if appid:
        # 外登录
        app_client = AppClient.get_by_app_id(appid)
        if app_client:
            # app id 验证成功
            appsecret = app_client.app_secret
            if not (
                callback_url and (callback_domain == app_client.app_domain or app_client.app_status == AppStatus.Beta)):
                callback_url = app_client.app_index_url
        else:
            # app id 验证失败
            return render_template('error.html', msg="AppId 验证失败")
    else:
        # 内登录
        if not (callback_url and callback_domain == request.host):
            callback_url = "http://{0}/".format(request.host)

    if pwd and login_name:
        user = account.login(login_name, pwd)

        if user:
            # 判断user 权限
            if can_user_login(user, app_client):
                access_token = AccessTokenModel(appid, user=user.cls2dict()).cls2token(appsecret)
                response = make_response(redirect(urlAddParam(callback_url, accesstoken=access_token)))
                if keeplogin:
                    id_token = IDTokenModel(user_id=user.id).cls2Token()
                    outdate = datetime.datetime.now() + datetime.timedelta(seconds=Config.ID_TOKEN_DEFAULT_EXPIRES)
                    response.set_cookie("idtoken", id_token, expires=outdate)
                return response
            else:
                return render_template('error.html', msg="没有权限访问")
        else:
            return render_template('login.html', msg="用户名密码错误", appid=appid if appid else "",
                                   callback_url=callback_url, keeplogin=keeplogin, pwd=pwd, name=login_name)
    else:
        return render_template('login.html', msg="填写信息不完整", appid=appid if appid else "",
                               callback_url=callback_url, keeplogin=keeplogin, pwd=pwd, name=login_name)


@app.route('/logout', methods=["GET"])
def logout():
    appid = request.args.get("appid", '')
    callback = request.args.get("callback", '')
    response = make_response(redirect("login?appid={0}&callback={1}".format(appid, callback)))
    response.delete_cookie('idtoken')
    response.delete_cookie('accesstoken')
    return response
