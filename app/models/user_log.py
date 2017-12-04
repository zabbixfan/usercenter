#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db
from datetime import date


class UserLog(db.Model):
    __tablename__ = "ax_user_log"
    log_date = db.Column(db.Date, primary_key=True)
    user_id = db.Column(db.String, primary_key=True)
    department_id_old = db.Column(db.BigInteger, default=0)
    department_id_new = db.Column(db.BigInteger, default=0)
    user_status_old = db.Column(db.String, default="")
    user_status_new = db.Column(db.String, default="")

    def save_to_today(self, auto_commit=True):
        self.log_date = date.today()
        log = UserLog.get(self.log_date, self.user_id)
        if log:
            db.session.query(UserLog).filter(UserLog.log_date == self.log_date).filter(
                UserLog.user_id == self.user_id).update({
                UserLog.department_id_new: self.department_id_new,
                UserLog.user_status_new: self.user_status_new
            })
        else:
            db.session.add(self)

        if auto_commit:
            db.session.commit()

    @staticmethod
    def get(log_date, user_id):
        return db.session.query(UserLog).filter(UserLog.user_id == user_id).filter(
            UserLog.log_date == log_date).first()
