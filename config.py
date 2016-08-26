# coding=utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    WTF_CSRF_ENABLED = False
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.kedacom.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'sqlmail@kedacom.com'
    MAIL_PASSWORD = '888'
    FLASKY_MAIL_SUBJECT_PREFIX = '[DTS]'
    FLASKY_MAIL_SENDER = 'DTS Admin <sqlmail@kedacom.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.05
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_DB_QUERY_TIMEOUT = 0.5

    # 分页参数
    FLASKY_POSTS_PER_PAGE = 20


    # 是否使用 mongodb
    MONGO_DB_USE = False
    # mongodb 数据库参数
    MONGO_HOST = '172.16.124.10'
    MONGO_PORT = 27017
    MONGO_DBNAME = 'test'

    # 附件存放目录和附件大小控制
    UPLOAD_FOLDER = os.path.join(basedir, 'attachments_files')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # 临时存放问题单数据导出文件
    OUTPUT_FOLDER = os.path.join(basedir, 'output_files')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI = "mysql://dts:123456@172.16.124.10:3306/dts_test"
    MONGO_DBNAME = 'dts'


class TestingConfig(Config):
    # 设置为true，不发送邮件通知
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    #SQLALCHEMY_DATABASE_URI = "mysql://dts:140327@127.0.0.1:3306/dts2"
    SQLALCHEMY_DATABASE_URI = "mysql://dts:123456@172.16.124.10:3306/dts"
    #SQLALCHEMY_ECHO = True
    MONGO_DBNAME = 'test'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': ProductionConfig
}
