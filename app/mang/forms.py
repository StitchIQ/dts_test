# coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import Required, Length


class Add_Product(Form):
    product_name = StringField(u'产品名称',
                               validators=[Required(), Length(1, 64)])
    product_descrit = StringField(u'产品描述',
                                  validators=[Required(), Length(1, 64)])
    product_status = RadioField(u'产品状态',
                                choices=[('1', '正常'), ('0', '禁用')],
                                default='1')

    submit = SubmitField('提交')


class Add_Software(Form):
    product_name = StringField('产品名称')
    product_descrit = StringField('产品描述')
    product_status = RadioField('产品状态',
                                choices=[('1', '正常'), ('0', '禁用')],
                                default='1')
    version_name = StringField('版本名称',
                               validators=[Required(), Length(1, 64)])
    version_descrit = StringField('版本描述',
                                  validators=[Required(), Length(1, 64)])
    software_version = StringField('软件版本列表', validators=[Required()])
    version_features = StringField('软件特性列表', validators=[Required()])
    submit = SubmitField('提交')
