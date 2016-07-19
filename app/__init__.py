# -*- coding: utf-8 -*-
import os
import logging
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config
from pymongo import MongoClient

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

mongodb = MongoClient('172.16.124.10',27017).test2


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    configure_logging(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .reports import reports as reports_blueprint
    app.register_blueprint(reports_blueprint)


    from .mang import mang as mang_blueprint
    app.register_blueprint(mang_blueprint, url_prefix='/mang')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


def configure_logging(app):
    """Configures logging."""

    import logging.config
    # 加载日志配置
    logging.config.fileConfig('app/config/logger.conf')
    #dts_log = logging.getLogger('dts')
    '''
    这个方法可以在全局使用app.logger.debug记录日志，
    logs_folder = os.path.join(app.root_path, os.pardir, "logs")
    from logging.handlers import SMTPHandler
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    info_log = os.path.join(logs_folder, "logs")

    info_file_handler = logging.handlers.RotatingFileHandler(
        info_log,
        maxBytes=100000,
        backupCount=10
    )
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)
    #app.logger.addHandler('dts')
    app.logger.debug("init______")
    '''
