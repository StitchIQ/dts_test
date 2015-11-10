#! /usr/bin/env python
#coding=utf-8
import os
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

@manager.command
def test():
	"""Run the unit tests"""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

"""
@app.route('/')
def index():
	return render_template('index.html')

@app.route("/base2")
def base2():
# 主页面
    return render_template('base2.html')


@app.route("/main")
def main():
# 主页面
    return render_template('main.html')

@app.route('/add')
def add_numbers():
    #Add two numbers server side, ridiculous but well...
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result = a + b)
"""


if __name__ == '__main__':
	manager.run()