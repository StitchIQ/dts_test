#coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField, \
        TextAreaField, RadioField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo



class Add_Product(Form):
    product_name = StringField('产品名称', validators=[Required(), Length(1, 64)])
    product_version = StringField('产品版本号', validators=[Required(), Length(1, 64)])
    software_version = StringField('软件版本号', validators=[Required(), Length(1, 64)])
    submit = SubmitField('提交')

