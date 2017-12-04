#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, redirect

from . import ctl as app


@app.app_errorhandler(404)
def error_404(error):
    return render_template('error_404.html'),404


@app.app_errorhandler(500)
def error_500(error):
    return render_template('error_500.html', msg=error),500


@app.app_errorhandler(405)
def error_405(error):
    return render_template('error_default.html', msg=error),405
