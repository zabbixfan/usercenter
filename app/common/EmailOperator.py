#!/usr/bin/env python
# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
import pyzmail

from config import Config


def GetSmtp():
    smtp = SMTP_SSL()
    smtp.connect(Config.EMALL_SMTP_HOST, Config.EMALL_SMTP_PORT)
    smtp.login(Config.EMALL_USER, Config.EMALL_PASSWORD)
    return smtp


def SendEmail(to_addrs, title, msg, type="plain", from_name=Config.EMALL_USER, toHander=None):
    mail_encoding = 'utf-8'
    # 发件人
    sender = (from_name, Config.EMALL_USER)
    # 收件人
    recipients = to_addrs
    if toHander is not None:
        recipients = toHander
    # 主题
    subject = title
    if type == 'html':
        payload, mail_from, rcpt_to, msg_id = pyzmail.compose_mail( \
            sender, \
            recipients, \
            subject, \
            mail_encoding, \
            ("", mail_encoding), \
            html=(msg, mail_encoding))
    else:
        payload, mail_from, rcpt_to, msg_id = pyzmail.compose_mail( \
            sender, \
            recipients, \
            subject, \
            mail_encoding, \
            (msg, mail_encoding), \
            html=None)
    try:
        smtp = GetSmtp()
        smtp.sendmail(Config.EMALL_USER, to_addrs, payload)
        return True
    except Exception, ex:
        print ex.message
        raise ex
        return False
