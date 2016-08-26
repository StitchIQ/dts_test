#! /usr/bin/env python
# coding=utf-8
import os
from app import create_app, db
from app.models import User, Role, Bugs, BugStatus, Process, ProductInfo, Bug_Now_Status
from flask_script import Manager, Shell, prompt, prompt_pass, prompt_bool
from flask_migrate import Migrate, MigrateCommand, upgrade
from sqlalchemy.exc import IntegrityError, OperationalError
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Bugs=Bugs,
                BugStatus=BugStatus, Process=Process, Bug_Now_Status=Bug_Now_Status)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def initdb():
    """Creates the database."""

    upgrade()


@manager.command
def dropdb():
    """Deletes the database."""

    db.drop_all()

@manager.command
def dts_init():
    u"""数据库初始化"""
    u"""首先执行数据库的初始化工作"""
    db.create_all()
    Role.insert_roles()
    BugStatus.insert_bug_status()
    print u'数据库初始化成功'


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_admin(username=None, password=None, email=None):
    """Creates the admin user."""

    if not (username and password and email):
        username = prompt("Username")
        email = prompt("A valid email address")
        password = prompt_pass("Password")

    u = User.create_admin_user(username=username, password=password, email=email)
    print("Creating admin user :%s Sucessful!" %u.username)

@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def install(username=None, password=None, email=None):
    """Installs DTS with all necessary data."""

    print("Creating default data...")
    try:
        Role.insert_roles()
        BugStatus.insert_bug_status()
    except IntegrityError:
        print("Couldn't create the default data because it already exist!")
        if prompt_bool("Found an existing database."
                       "Do you want to recreate the database? (y/n)"):
            db.session.rollback()
            db.drop_all()
            db.create_all()
            print("Creating DataBase Default Data...")
            Role.insert_roles()
            BugStatus.insert_bug_status()
        else:
            sys.exit(0)
    except OperationalError:
        print("No database found.")
        if prompt_bool("Do you want to create the database now? (y/n)"):
            db.session.rollback()
            db.drop_all()
            db.create_all()
            print("Creating DataBase Default Data...")
            Role.insert_roles()
            BugStatus.insert_bug_status()
        else:
            sys.exit(0)

    print("Creating admin user...")
    if username and password and email:
        User.create_admin_user(username=username, password=password, email=email)
    else:
        create_admin()

    dir_create()
    print("Congratulations! DTS has been successfully installed")

@manager.command
def dir_create():
    u"""创建运行需要的文件夹"""
    UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
    OUTPUT_FOLDER = app.config['OUTPUT_FOLDER']

    if not os.path.exists(UPLOAD_FOLDER): #如果目录不存在就返回False
        os.makedirs(UPLOAD_FOLDER)
        print u'创建 %s 目录成功' %UPLOAD_FOLDER
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print u'创建 %s 目录成功' % OUTPUT_FOLDER


@manager.command
def database_upgrade():
    u"""升级数据库"""
    from flask.ext.migrate import upgrade, migrate
    migrate()
    upgrade()
    print u'数据库升级成功'


@manager.command
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    # python manage.py runserver -h 127.0.0.1 -p 8000 带参数运行这个命令
    manager.run()
    #app.run(host="0.0.0.0", port=8080)
