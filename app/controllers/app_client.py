#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, g, request, abort, redirect, jsonify

from . import ctl as app
from ..common import alopex_auth_sdk
from ..domain import app_domain


@app.route("/app/add", methods=["GET"])
@alopex_auth_sdk.need_login()
def add_app_view():
    return render_template('add_app.html', user=g.user)


@app.route("/app/list", methods=["GET"])
@alopex_auth_sdk.need_login()
def app_list_view():
    apps = app_domain.getAppsByUser(g.user.get("id"))
    outlink_apps = app_domain.getOutlinkAppsByUser(g.user.get("id"))
    return render_template('app_manage_list.html', user=g.user, apps=apps, outlinkApps=outlink_apps)


@app.route("/app/add", methods=["POST"])
@alopex_auth_sdk.need_login()
def add_app():
    name = request.form.get("name")
    desc = request.form.get("desc")
    domain = request.form.get("domain")
    index = request.form.get("index")
    repo = request.form.get("repo")
    logo_color = request.form.get("color")
    logo = request.form.get("logo")
    status = request.form.get("status")
    default_access_status = request.form.get("defaultAccessStatus")
    app = app_domain.addApp(g.user.get("id"), name, domain, index, desc, repo, logo_color, logo, status, default_access_status)

    return redirect('/app/info/{0}'.format(app.app_id))


@app.route("/outlinkapp/add", methods=["POST"])
@alopex_auth_sdk.need_login()
def add_outlink_app():
    name = request.form.get("name")
    index = request.form.get("index")
    logo_color = request.form.get("color")
    logo = request.form.get("logo")
    desc = request.form.get("desc")
    status = request.form.get("status")

    app = app_domain.addOutlinkApp(g.user.get("id"), name, index, logo_color, logo, desc, status)
    return redirect('/outlinkapp/info/{0}'.format(app.outlink_id))


@app.route("/app/info/<appid>", methods=["GET"])
@alopex_auth_sdk.need_login()
def app_info(appid):
    app = app_domain.getAppById(appid)
    if app and app.app_manager == g.user.get("id"):
        return render_template("app_info.html", user=g.user, app=app)
    else:
        abort(404)


@app.route("/outlinkapp/info/<appid>", methods=["GET"])
@alopex_auth_sdk.need_login()
def outlink_app_info(appid):
    app = app_domain.getOutlinkAppById(appid)
    if app and app.outlink_manager == g.user.get("id"):
        return render_template("outlink_app_info.html", user=g.user, app=app)
    else:
        abort(404)


@app.route("/app/edit/<appid>", methods=["GET"])
@alopex_auth_sdk.need_login()
def edit_app_view(appid):
    app = app_domain.getAppById(appid)
    if app and app.app_manager == g.user.get("id"):
        return render_template("edit_app.html", user=g.user, app=app)
    else:
        abort(404)


@app.route("/app/edit/<appid>", methods=["POST"])
@alopex_auth_sdk.need_login()
def edit_app(appid):
    name = request.form.get("name")
    desc = request.form.get("desc")
    domain = request.form.get("domain")
    index = request.form.get("index")
    repo = request.form.get("repo")
    logo_color = request.form.get("color")
    logo = request.form.get("logo")
    status = request.form.get("status")
    default_access_status = request.form.get("defaultAccessStatus")
    app_domain.updateApp(appid, g.user.get("id"), name, index, domain, repo, logo_color, logo, desc, status, default_access_status)
    return redirect('/app/info/' + appid)


@app.route("/outlinkapp/edit/<appid>", methods=["GET"])
@alopex_auth_sdk.need_login()
def edit_outlink_app_view(appid):
    app = app_domain.getOutlinkAppById(appid)
    if app and app.outlink_manager == g.user.get("id"):
        return render_template("edit_outlinkapp.html", user=g.user, app=app)
    else:
        return abort(404)


@app.route("/outlinkapp/edit/<appid>", methods=["POST"])
@alopex_auth_sdk.need_login()
def edit_outlink_app(appid):
    name = request.form.get("name")
    index = request.form.get("index")
    logo_color = request.form.get("color")
    logo = request.form.get("logo")
    desc = request.form.get("desc")
    status = request.form.get("status")

    app_domain.updateOutlinkApp(appid, g.user.get("id"), name, index, logo_color, logo, desc, status)
    return redirect('/outlinkapp/info/' + appid)


@app.route('/app/delete/<appid>', methods=["POST"])
@alopex_auth_sdk.need_login()
def deleteApp(appid):
    app_domain.deleteApp(appid, g.user.get("id"))
    return jsonify({"status": "success"})


@app.route('/outlinkapp/delete/<appid>', methods=["POST"])
@alopex_auth_sdk.need_login()
def deleteOutlinkApp(appid):
    try:
        app_domain.deleteOutlinkApp(appid, g.userID)
        return jsonify({"status": "success"})
    except:
        return None
