#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db


class Role(db.Model):
    __tablename__ = "ax_role"
    user_id = db.Column(db.String(32), primary_key=True)
    app_id = db.Column(db.String(32), primary_key=True)
    role_code = db.Column(db.String(50))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, user_id, app_id):
        db.session.query(cls).filter(cls.user_id == user_id).filter(cls.app_id == app_id).delete()
        db.session.commit()

    @classmethod
    def get(cls, user_id, app_id):
        return db.session.query(cls).filter(cls.user_id == user_id).filter(cls.app_id == app_id).first()

    @classmethod
    def batchAdd(cls, users, app_id, role_code):
        for user in users:
            role = db.session.query(Role).filter(Role.app_id == app_id).filter(Role.user_id == user).first()
            if not role:
                role = Role()
                role.user_id = user
                role.app_id = app_id
                role.role_code = role_code
                db.session.add(role)
                db.session.flush()
            else:
                db.session.query(Role).filter(Role.app_id == app_id).filter(Role.user_id == user).update({
                    Role.role_code: role_code
                })
                db.session.flush()
        db.session.commit()