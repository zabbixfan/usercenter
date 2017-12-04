#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Employee(object):
    def __init__(self, uuid, name, empno, department_uuid, mobile, exmail, email, sex, job_title, join_date, leave_date,
                 status, dingtalk_id, job_grade, phone_number, id_number, address, bank_card, photo, marriage, birthday,
                 avatar, nickname, leader_uuid, virtual_leader_uuid):
        self.uuid = uuid
        self.name = name
        self.sex = sex
        self.empno = empno
        self.email = email
        self.mobile = mobile
        self.phone_number = phone_number
        self.id_number = id_number
        self.address = address
        self.bank_card = bank_card
        self.photo = photo
        self.marriage = marriage
        self.birthday = birthday
        self.join_date = join_date
        self.avatar = avatar
        self.leave_date = leave_date
        self.status = status
        self.department_uuid = department_uuid
        self.exmail = exmail
        self.job_title = job_title
        self.job_grade = job_grade
        self.dingtalk_id = dingtalk_id
        self.nickname = nickname
        self.leader_uuid = leader_uuid
        self.virtual_leader_uuid = virtual_leader_uuid

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
                   data_dict.get("job_grade"),
                   data_dict.get("phone_number"),
                   data_dict.get("id_number"),
                   data_dict.get("address"),
                   data_dict.get("bank_card"),
                   data_dict.get("photo"),
                   data_dict.get("marriage"),
                   data_dict.get("birthday"),
                   data_dict.get("avatar"),
                   data_dict.get("nickname"),
                   data_dict.get("leader_uuid"),
                   data_dict.get("virtual_leader_uuid")
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
            "dingtalk_id": self.dingtalk_id,
            "phone_number": self.phone_number,
            "address": self.address,
            "id_number": self.id_number,
            "bank_card": self.bank_card,
            "photo": self.photo,
            "marriage": self.marriage,
            "avatar": self.avatar,
            "nickname": self.nickname,
            "leader_uuid": self.leader_uuid,
            "virtual_leader_uuid": self.virtual_leader_uuid
        }
