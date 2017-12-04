#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Employee(object):
    def __init__(self, uuid, name, empno, department_uuid, mobile, exmail, email, sex, job_title, join_date, leave_date,
                 status, dingtalk_id, job_grade):
        self.uuid = uuid
        self.name = name
        self.empno = empno
        self.department_uuid = department_uuid
        self.mobile = mobile
        self.exmail = exmail
        self.email = email
        self.sex = sex
        self.job_title = job_title
        self.join_date = join_date
        self.leave_date = leave_date
        self.status = status
        self.dingtalk_id = dingtalk_id
        self.job_grade = job_grade

    @classmethod
    def dict2cls(cls, data_dict):
        return cls(data_dict.get("uuid"),
                   data_dict.get("name"),
                   data_dict.get("empno"),
                   data_dict.get("department_uuid"),
                   data_dict.get("mobile"),
                   data_dict.get("exmail"),
                   data_dict.get("email"),
                   data_dict.get("sex"),
                   data_dict.get("job_title"),
                   data_dict.get("join_date"),
                   data_dict.get("leave_date"),
                   data_dict.get("status"),
                   data_dict.get("dingtalk_id"),
                   data_dict.get("job_grade")
                   )

    def cls2dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "empno": self.empno,
            "department_uuid": self.department_uuid,
            "mobile": self.mobile,
            "exmail": self.exmail,
            "email": self.email,
            "sex": self.sex,
            "job_title": self.job_title,
            "join_date": self.join_date,
            "leave_date": self.leave_date,
            "status": self.status,
            "job_grade": self.job_grade,
            "dingtalk_id": self.dingtalk_id
        }
