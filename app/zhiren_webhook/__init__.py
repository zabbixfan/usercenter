#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

zhiren_webhook = Blueprint('zhiren_webhook', __name__,url_prefix="/zhiren")

import webhook