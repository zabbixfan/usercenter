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
from app import cache
import random,json,re
from app.common.aliyunMNS import aliyunMsg
from app.models.user import User

@app.route("/msglogin", methods=["GET"])
def msglogin():
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
    return render_template('login_msg.html', callback_url=callback_url, appid=appid)
@app.route("/setcode", methods=["POST"])
def setCode():
    phone = request.form.get('phone')
    q = User.query.filter(User.user_mobile == phone).first()
    if not q:
        return "手机号不合法"
    phone_count = cache.get("{}_count".format(phone))
    print phone_count
    if phone_count is None:
        cache.set("{}_count".format(phone),1,timeout=60)
    else:
        phone_count += 1
        cache.set("{}_count".format(phone),phone_count,timeout=60)
    if phone_count > 2:
        return "发送次数过多"
    code = cache.get(phone)
    if code is None:
        code = random.randint(100000,999999)
        cache.set(phone,code,timeout=3*60)
    aliyunMsg(phone,str(code),'')
    return "发送成功"

@app.route("/getcode/<phone>",methods=["GET"])
def getCode(phone):
    code = cache.get(phone)
    print code
    return "查询成功"

@app.route("/msglogin", methods=["POST"])
def msgauthorize():
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
        code = cache.get(login_name)
        params = re.compile(r'^\d{6}$')
        if params.findall(pwd):
            if code == int(pwd):
                access_token = AccessTokenModel(appid, user=login_name).cls2token(appsecret)
                response = make_response(redirect(urlAddParam(callback_url, accesstoken=access_token)))
                return response
            # if user:
            #     # 判断user 权限
            #     if can_user_login(user, app_client):
            #         access_token = AccessTokenModel(appid, user=user.cls2dict()).cls2token(appsecret)
            #         response = make_response(redirect(urlAddParam(callback_url, accesstoken=access_token)))

                # else:
                #     return render_template('error.html', msg="没有权限访问")
            else:
                return render_template('login_msg.html', msg="用户名密码错误", appid=appid if appid else "",
                                       callback_url=callback_url, keeplogin=keeplogin, pwd=pwd, name=login_name)
        else:
            return render_template('login_msg.html', msg="验证码格式有误", appid=appid if appid else "",
                                   callback_url=callback_url, keeplogin=keeplogin, pwd=pwd, name=login_name)
    else:
        return render_template('login_msg.html', msg="填写信息不完整", appid=appid if appid else "",
                                   callback_url=callback_url, keeplogin=keeplogin, pwd=pwd, name=login_name)


