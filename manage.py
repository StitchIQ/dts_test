#! /usr/bin/env python
#coding=utf-8
import os
from app import create_app, db
from app.models import User, Role, Bugs, BugStatus, Process, ProductInfo
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role, Bugs=Bugs,
		BugStatus=BugStatus, Process=Process)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

@manager.command
def test():
	"""Run the unit tests"""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)



if __name__ == '__main__':
	manager.run()
	#app.run(host="0.0.0.0",port=8000)