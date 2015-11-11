#coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class StandardBug(Form):
    wentimiaoshu = StringField('Email', validators=[Required(), Length(1, 64)])
    chanpinmingcheng = StringField('Email', validators=[Required(), Length(1, 64)])
    banbenhao = StringField('Email', validators=[Required(), Length(1, 64)])
    yanzhongxing = StringField('Email', validators=[Required(), Length(1, 64)])
    ceshibuzhou = StringField('Email', validators=[Required(), Length(1, 64)])
    xitongbiaoxian = StringField('Email', validators=[Required(), Length(1, 64)])
    chuxianpinlv = StringField('Email', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('提交')
