#!/usr/bin/env python
# -*- coding: utf-8 -*-

def urlAddParam(url="", **kwargs):
    param_str = url.strip()
    param_str = param_str.replace('%23','#')
    if '?' in param_str:
        param_str += "&"
    else:
        param_str += "?"
    for key, value in kwargs.iteritems():
        param_str += "{0}={1}&".format(key, value)
    return param_str
