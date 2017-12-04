#!coding:utf-8
from mns.account import Account
from mns.queue import *
from mns.topic import TopicMessage
from mns.topic import DirectSMSInfo
import sys
from config import Config

def aliyunMsg(user,*args):
    code,product = args
    my_account = Account(Config.MNS_ENDPOINT, Config.MNS_ACCESSID, Config.MNS_ACCESSKEY)
    my_topic = my_account.get_topic(Config.MNS_TOPIC)
    msg_body1 = "sms-message1."
    direct_sms_attr1 = DirectSMSInfo(free_sign_name=Config.MNS_SIGN,template_code=Config.MNS_TEMPLATE_CODE,single=True)
    direct_sms_attr1.add_receiver(receiver=user)
    direct_sms_attr1.set_params({"code": code,"product": product})
    msg1 = TopicMessage(msg_body1, direct_sms = direct_sms_attr1)
    try:
        re_msg = my_topic.publish_message(msg1)
        print "Publish Message Succeed. MessageBody:%s MessageID:%s" % (msg_body1, re_msg.message_id)
    except MNSExceptionBase,e:
        if e.type == "TopicNotExist":
            print "Topic not exist, please create it."
            sys.exit(1)
        print "Publish Message Fail. Exception:%s" % e
    return "message send"
