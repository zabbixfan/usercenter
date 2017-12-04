#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, g


from . import ctl as app
from ..common import alopex_auth_sdk
from ..domain import app_domain

@app.route("/", methods=["GET"])
@alopex_auth_sdk.need_login()
def index():

    apps = app_domain.getOnlineAppByUserCanView(g.userID)
    outlinkapps = app_domain.getOnlineOutlinkApp()

    return render_template('index.html', user=g.user,apps=apps,outlinkapps=outlinkapps)
