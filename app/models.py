#coding=utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import bleach
from markdown import markdown
from flask import current_app, url_for

from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager




class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Bug_Now_Status:
    CREATED = 1
    TESTLEADER_AUDIT = 2
    DEVELOPMENT = 3
    TESTLEADER_REGESSION = 4
    REGRESSION_TESTING = 5
    CLOSED = 6

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class VersionInfo(db.Model):
    __tablename__ = 'versioninfo'
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('productinfo.id'))
    version_name = db.Column(db.Text)
    version_descrit = db.Column(db.Text)
    software_version = db.Column(db.Text)
    version_features  = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True,default=datetime.utcnow)
    update_time = db.Column(db.DateTime, index=True,default=datetime.utcnow)

    def software_to_json(self):
        json_post = {
            'software': self.version_name,
            'version': self.software_version,
            'features': self.version_features,
            }
        return json_post

    #返回版本的信息
    def version_to_turple(self):

        return (self.version_name, self.version_name)

    #返回软件版本的信息
    def software_to_turple(self):
        dd = []
        for soft in self.software_version.split(';'):
            dd.append((soft,soft))
        return dd

    #返回软件特性的信息
    def features_to_turple(self):
        dd = []
        for features in self.version_features.split(';'):
            dd.append((features,features))
        return dd

class ProductInfo(db.Model):
    __tablename__ = 'productinfo'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(64),unique=True)
    product_descrit = db.Column(db.Text)
    product_status = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, index=True,default=datetime.utcnow)
    update_time = db.Column(db.DateTime, index=True,default=datetime.utcnow)

    p_id = db.relationship('VersionInfo',
                            foreign_keys=[VersionInfo.product],
                            backref='software', lazy='dynamic')

    def product_name_json(self):
        json_post = {
            'name': self.product_name,
            }
        return json_post

    def product_name_turple(self):

        return (self.product_name, self.product_name)

class Process(db.Model):
    __tablename__ = 'process'
    id = db.Column(db.Integer,primary_key=True)
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bugs_id = db.Column(db.Integer, db.ForeignKey('bugs.id'))
    old_status = db.Column(db.Integer, db.ForeignKey('bugstatus.bug_status'))
    new_status = db.Column(db.Integer, db.ForeignKey('bugstatus.bug_status'))
    opinion = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True,default=datetime.utcnow)


class Bugs(db.Model):
    __tablename__ = 'bugs'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_name = db.Column(db.String(64))
    product_version = db.Column(db.String(64))
    software_version = db.Column(db.String(64))
    version_features = db.Column(db.String(64))
    bug_level = db.Column(db.String(64))
    system_view = db.Column(db.String(64))
    bug_show_times = db.Column(db.String(64))
    bug_title = db.Column(db.String(64))
    bug_descrit = db.Column(db.Text)
    bug_descrit_html = db.Column(db.Text)
    bug_owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bug_status = db.Column(db.Integer, db.ForeignKey('bugstatus.bug_status'))
    bug_photos = db.Column(db.Text)
    resolve_version = db.Column(db.String(64))
    regression_test_version = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    bug_last_update = db.Column(db.DateTime(), default=datetime.utcnow)


    process = db.relationship('Process',
                            foreign_keys=[Process.bugs_id],
                            backref='bugs', lazy='dynamic')


    def __repr__(self):
        return '<User %r>' % self.id

    def to_json(self):
        json_post = {
            'url': url_for('main.bug_process', id=self.id, _external=True),
            'id': self.id,
            'author': self.author.username,
            'product_name':self.product_name,
            'product_version':self.product_version,
            'software_version':self.software_version,
            'bug_level':self.bug_level,
            'system_view':self.system_view,
            'bug_show_times': self.bug_show_times,
            'bug_title': self.bug_title,
            'bug_owner': self.bug_owner.username,
            'bug_status': self.now_status.bug_status_descrit,
            'timestamp': self.timestamp
            }
        return json_post

    def ping(self):
        self.bug_last_update = datetime.utcnow()
        db.session.add(self)

    @staticmethod
    def on_changed_bug_descrit(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.bug_descrit_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Bugs.bug_descrit, 'set', Bugs.on_changed_bug_descrit)


class BugStatus(db.Model):
    __tablename__ = 'bugstatus'
    id = db.Column(db.Integer, primary_key=True)
    bug_status = db.Column(db.Integer)
    bug_status_descrit = db.Column(db.String(64))

    old_status = db.relationship('Process',foreign_keys=[Process.old_status],
                                backref='old',lazy='dynamic')

    new_status = db.relationship('Process',foreign_keys=[Process.new_status],
                                    backref='new',lazy='dynamic')

    bug_now_status = db.relationship('Bugs',foreign_keys=[Bugs.bug_status],
                                    backref='now_status',lazy='dynamic')



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    bugs = db.relationship('Bugs',
                           foreign_keys=[Bugs.author_id],
                           backref='author', lazy='dynamic')

    bugs_owner = db.relationship('Bugs',
                                 foreign_keys=[Bugs.bug_owner_id],
                                 backref='bug_owner', lazy='dynamic')

    process = db.relationship('Process',
                            foreign_keys=[Process.author_id],
                            backref='author', lazy='dynamic')
    operators = db.relationship('Process',
                            foreign_keys=[Process.operator_id],
                            backref='operator', lazy='dynamic')


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser