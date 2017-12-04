#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db


class Department(db.Model):
    __tablename__ = 'ax_department'

    department_id = db.Column(db.BigInteger, primary_key=True)
    department_name = db.Column(db.String(255))
    parent_department = db.Column(db.BigInteger, default=0)
    zhiren_uuid = db.Column(db.String(32), default="")
    is_del = db.Column(db.Boolean, default=False)

    @classmethod
    def get_by_zhiren_uuid(cls, uuid):
        if uuid:
            rel = db.session.query(cls).filter(cls.zhiren_uuid == uuid).first()
            return rel
        return None

    def save(self):
        db.session.add(self)
        db.session.flush()

    @classmethod
    def commit(cls):
        db.session.commit()

    @classmethod
    def get_by_id(cls, department_id):
        return db.session.query(cls).filter(
            Department.department_id == department_id).filter(
                Department.is_del == False).first()

    @classmethod
    def get_all_sub_list(cls, department_id):
        rel = []
        first_level = db.session.query(cls).filter(
            Department.parent_department == department_id).filter(
                Department.is_del == False).all()
        rel += first_level
        for dep in first_level:
            rel += cls.get_all_sub_list(dep.department_id)
        return rel
