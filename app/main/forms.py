#coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
        TextAreaField, RadioField, SelectField,FileField, validators, FieldList
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField

from flask_wtf.file import FileField,FileRequired,FileAllowed
import os


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required(), Email()])
    submit = SubmitField('Submit')

class MySelectField(SelectField):

    def pre_validate(self, form):
        print 'myselcect ssssss'
        print self.data
        print 'ssssss222222'
        if str(self.data) != '-1':
            pass
        else:
            raise ValueError(self.gettext('Not a valid choice44444'))

class StandardBug(Form):
    #product_name = StringField('产品名称', validators=[Required(), Length(1, 64)])
    #product_version = StringField('产品版本号', validators=[Required(), Length(1, 64)])
    #software_version = StringField('软件版本号', validators=[Required(), Length(1, 64)])
    product_name = SelectField('产品名称',coerce=str, choices=[])
    product_version = MySelectField('产品版本号', coerce=str, choices=[])
    software_version = MySelectField('软件版本号', coerce=str, choices=[('-1',u'请选择产品')])
    version_features = MySelectField('软件特性', choices=[])
    #bug_level = StringField('严重程度', validators=[Required(), Length(1, 64)])
    bug_level = SelectField('严重程度', choices=[('致命','致命'),('严重','严重'),('一般','一般'),('提示','提示')])
    system_view = StringField('系统表现', validators=[Required(), Length(1, 64)])
    #bug_show_times = StringField('出现频率', validators=[Required(), Length(1, 64)])
    bug_show_times = SelectField('出现频率', choices=[('必现','必现'),('频繁出现','频繁出现'),('概率出现','概率出现'),('较难重现','较难重现'),('无法重现','无法重现')])
    bug_title = StringField('问题标题', validators=[Required(), Length(1, 64)])
    bug_descrit = PageDownField('问题描述', validators=[Required()])
    #bug_descrit = StringField('问题描述', validators=[Required(), Length(1, 64)])
    bug_owner_id = StringField('问题处理人', validators=[Required(), Email()])
    bug_status = RadioField('选择处理', choices=[('1', '新建'),('2', '测试经理审核')], default='1')
    #save = SubmitField('保存')
    #photo = FileField('DTS phote',validators=[FileRequired(),FileAllowed(['jpg','jpeg'],'EEEE')])
    photo = FileField('DTS phote')
    submit = SubmitField('提交')

class BugsProcess(Form):
    product_name = StringField('产品名称')
    product_version = StringField('产品版本号')
    software_version = StringField('软件版本号')
    version_features = StringField('软件特性')
    bug_level = StringField('严重程度')
    system_view = StringField('系统表现')
    bug_show_times = StringField('出现频率')
    bug_title = StringField('问题标题')
    bug_descrit = TextAreaField('问题描述')

    #bug_owner_id = StringField('问题处理人')

class TestLeadEdit(Form):
    test_process_opinion = TextAreaField('处理意见', validators=[Required()])
    bug_owner_id = StringField('问题单处理人', validators=[Required(), Email()])
    bug_status = RadioField('选择处理', choices=[('1', '返回修改'),('3', '开发人员修改')], default='3')
    submit = SubmitField('提交')


class DevelopEdit(Form):
    deve_process_opinion = TextAreaField('处理意见', validators=[Required()])
    resolve_verson = SelectField('解决版本',choices=[],validators=[Required()])
    # names = FieldList(StringField('名称'), label='物品列表', min_entries=1)
    bug_owner_id = StringField('问题单处理人', validators=[Required(), Email()])
    #resolve_verson = SelectField('解决版本', choices=[('致命','致命'),('严重','严重'),('一般','一般'),('提示','提示')])
    bug_status = RadioField('选择处理', choices=[('2', '返回测试经理'),('3', '转交其他开发人员处理'),('4', '测试经理组织回归测试')],default='4',validators=[Required()])
    submit = SubmitField('提交')

    def __init__(self):
        Form.__init__(self)
        #self.resolve_verson = SelectField('解决版本', choices=ss)


class TestLeadEdit2(Form):
    process_opinion = TextAreaField('处理意见', validators=[Required()])
    bug_owner_id = StringField('问题单处理人', validators=[Required(), Email()])
    bug_status = RadioField('选择处理', choices=[('3', '返回开发人员修改'),('5', '测试人员回归')],default='5')
    submit = SubmitField('提交')

class BugClose(Form):
    regression_test_version = SelectField('回归测试版本',choices=[])
    process_opinion = TextAreaField('处理意见', validators=[Required()])
    #bug_owner_id = StringField('问题单处理人', validators=[Required(), Email()])
    bug_status = RadioField('选择处理', choices=[('6', '问题关闭'),('4', '测试经理组织回归测试')], default='6')
    submit = SubmitField('提交')
