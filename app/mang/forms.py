#coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField, \
        TextAreaField, RadioField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo



class Add_Product(Form):
    product_name = StringField('产品名称', validators=[Required(), Length(1, 64)])
    product_descrit = StringField('产品描述', validators=[Required(), Length(1, 64)])
    submit = SubmitField('提交')

class Add_Software(Form):
    product_name = StringField('产品名称')
    product_descrit = StringField('产品描述')
    version_name = StringField('版本名称', validators=[Required(), Length(1, 64)])
    version_descrit = StringField('版本描述', validators=[Required(), Length(1, 64)])
    software_version = StringField('软件版本列表', validators=[Required()])
    submit = SubmitField('提交')