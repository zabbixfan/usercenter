#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
import config
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
db = SQLAlchemy()


def logger_init(name="root"):
    """
    log 初始化
    :param name:
    :return:
    """
    logger = logging.getLogger(name)
    handler = logging.FileHandler('app.log', encoding='utf-8')
    logging_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s")
    handler.setFormatter(logging_format)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def logger(name="root"):
    """
    日志 logger
    :param name:
    :return:
    """
    return logging.getLogger(name)


def create_app():
    import controllers
    import zhiren_webhook
    import api
    app = Flask(__name__, instance_relative_config=True)
    # 注册配置文件
    app.config.from_object(config.Config)
    db.init_app(app)
    # 注册 Blueprint
    app.register_blueprint(controllers.ctl)
    app.register_blueprint(zhiren_webhook.zhiren_webhook)
    # CORS
    CORS(app, resources={r"/api/*": {"origins": config.Config.CORS_ORIGINS}})
    api.api.init_app(app)
    # LOG
    logger_init()
    return app
