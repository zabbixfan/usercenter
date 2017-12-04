#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db
from .app_client import AppStatus


class OutlinkApp(db.Model):
    __tablename__ = "ax_outlink_app"
    outlink_id = db.Column(db.BigInteger, primary_key=True)
    outlink_name = db.Column(db.String(20))
    outlink_description = db.Column(db.String(255), default="")
    outlink_logo = db.Column(db.String(255), default="")
    outlink_logo_color = db.Column(db.String(10), default="#2196F3")
    outlink_index_url = db.Column(db.String(255), default="")
    outlink_manager = db.Column(db.String(32))
    outlink_status = db.Column(db.String(10), default=AppStatus.Beta)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def getById(cls, aid):
        return db.session.query(cls).filter(cls.outlink_id == aid).first()
