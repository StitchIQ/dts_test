#coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class StandardBug(Form):
    product_name = StringField('产品名称', validators=[Required(), Length(1, 64)])
    product_version = StringField('产品版本号', validators=[Required(), Length(1, 64)])
    software_version = StringField('软件版本号', validators=[Required(), Length(1, 64)])
    bug_level = StringField('严重程度', validators=[Required(), Length(1, 64)])
    system_view = StringField('系统表现', validators=[Required(), Length(1, 64)])
    bug_show_times = StringField('出现频率', validators=[Required(), Length(1, 64)])
    bug_title = StringField('问题标题', validators=[Required(), Length(1, 64)])
    bug_descrit = PageDownField("问题描述", validators=[Required()])
    #bug_descrit = StringField('问题描述', validators=[Required(), Length(1, 64)])
    bug_owner_id = StringField('问题处理人', validators=[Required(), Email()])

    save = SubmitField('保存')
    submit = SubmitField('提交')

class BugsProcess(Form):
    bug_descrit = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')