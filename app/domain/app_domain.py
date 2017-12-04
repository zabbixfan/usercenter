#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db
from ..models.app_client import AppClient, AppStatus, DefaultAccessStatus
from ..models.outlink_app import OutlinkApp
from ..domain.role_domain import Role


def addApp(user, name, domain, index, desc, repo, color, logo, status, default_access_status):
    client = AppClient()
    client.app_name = name
    client.app_description = desc
    client.app_domain = domain
    client.app_index_url = index
    client.app_code_repo = repo
    client.app_logo_color = color
    client.app_logo = logo
    client.app_manager = user
    client.app_status = status
    client.default_access_status = default_access_status
    client.add()
    return client


def addOutlinkApp(user, name, index, color, logo, desc, status):
    outlink = OutlinkApp()
    outlink.outlink_name = name
    outlink.outlink_index_url = index
    outlink.outlink_logo_color = color
    outlink.outlink_logo = logo
    outlink.outlink_manager = user
    outlink.outlink_description = desc
    outlink.outlink_status = status

    outlink.add()
    return outlink


def getAppById(app_id):
    return AppClient.get(app_id)


def getAppsByUser(user):
    apps = db.session.query(AppClient).filter(AppClient.app_manager == user).filter(
        AppClient.app_status != AppStatus.Delete).all()
    return apps


def getOutlinkAppsByUser(user):
    apps = db.session.query(OutlinkApp).filter(OutlinkApp.outlink_manager == user).filter(
        OutlinkApp.outlink_status != AppStatus.Delete).all()
    return apps


def getOutlinkAppById(app_id):
    return OutlinkApp.getById(app_id)


def updateApp(appid, user, name, index, domain, repo, color, logo, desc, status, default_access_status):
    db.session.query(AppClient).filter(AppClient.app_id == appid).filter(AppClient.app_manager == user).update({
        AppClient.app_name: name,
        AppClient.app_index_url: index,
        AppClient.app_domain: domain,
        AppClient.app_logo_color: color,
        AppClient.app_logo: logo,
        AppClient.app_description: desc,
        AppClient.app_status: status,
        AppClient.app_code_repo: repo,
        AppClient.default_access_status: default_access_status
    })
    db.session.commit()


def updateOutlinkApp(appid, user, name, index, color, logo, desc, status):
    db.session.query(OutlinkApp).filter(OutlinkApp.outlink_id == appid).filter(
        OutlinkApp.outlink_manager == user).update({
        OutlinkApp.outlink_name: name,
        OutlinkApp.outlink_index_url: index,
        OutlinkApp.outlink_logo_color: color,
        OutlinkApp.outlink_logo: logo,
        OutlinkApp.outlink_description: desc,
        OutlinkApp.outlink_status: status
    })

    db.session.commit()


def getOnlineApp():
    return db.session.query(AppClient).filter(AppClient.app_status == AppStatus.Online).all()


def getOnlineOutlinkApp():
    return db.session.query(OutlinkApp).filter(OutlinkApp.outlink_status == AppStatus.Online).all()


def deleteApp(appid, user):
    db.session.query(AppClient).filter(AppClient.app_id == appid).filter(AppClient.app_manager == user).update({
        AppClient.app_status: AppStatus.Delete
    })
    db.session.commit()


def deleteOutlinkApp(appid, user):
    db.session.query(OutlinkApp).filter(OutlinkApp.outlink_id == appid).filter(
        OutlinkApp.outlink_manager == user).update({
        OutlinkApp.outlink_status: AppStatus.Delete
    })
    db.session.commit()


def getOnlineAppByUserCanView(userId):
    return db.session.query(AppClient).outerjoin(Role, AppClient.app_id == Role.app_id).filter(
        AppClient.app_status == AppStatus.Online) \
        .filter(db.or_(AppClient.default_access_status == DefaultAccessStatus.Allow,
                       db.and_(AppClient.default_access_status == DefaultAccessStatus.NotAllow,
                               Role.user_id == userId))).all()
