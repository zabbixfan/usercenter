#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db
from werkzeug.security import gen_salt
from uuid import uuid1 as uuid


class AppStatus(object):
    Online = "online"
    Beta = "beta"
    Delete = "delete"

class DefaultAccessStatus(object):
    NotAllow = 'NotAllow'
    Allow = 'Allow'



class AppClient(db.Model):
    __tablename__ = "ax_app"
    app_id = db.Column(db.String(32), primary_key=True)
    app_secret = db.Column(db.String(40))
    app_name = db.Column(db.String(20))
    app_description = db.Column(db.String(255), default="")
    app_logo = db.Column(db.String(255), default="")
    app_logo_color = db.Column(db.String(10), default="#2196F3")
    app_domain = db.Column(db.String(255), default="")
    app_index_url = db.Column(db.String(255), default="")
    app_code_repo = db.Column(db.String(255), default="")
    app_manager = db.Column(db.String(32))
    app_status = db.Column(db.String(10), default=AppStatus.Beta)
    default_access_status = db.Column(db.String(25), default=DefaultAccessStatus.NotAllow)

    @classmethod
    def verify_appid(cls, app_id, domain):
        rel = db.session.query(cls).filter(cls.app_id == app_id) \
            .filter(cls.app_domain == domain).first()
        return True if rel else False

    @classmethod
    def get_by_app_id(cls, app_id):
        return db.session.query(cls).filter(cls.app_id == app_id) \
            .filter(cls.app_status != AppStatus.Delete).first()

    def add(self):
        self.app_id = uuid().get_hex()
        self.app_secret = gen_salt(40)
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get(cls, appid):
        return db.session.query(cls).filter(cls.app_id == appid).first()
