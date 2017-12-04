#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import Config

SECRET_KEY = Config.ZHIREN_SECRET_KEY
APP_KEY = Config.ZHIRRN_APP_KEY

from .signature import verify_signature