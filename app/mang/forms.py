# coding=utf-8
from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import Required, Length


class Add_Product(Form):
    product_name = StringField(u'产品名称',
                               validators=[Required(), Length(1, 64)],render_kw={"placeholder": u"请输入产品名称"})
    product_descrit = StringField(u'产品描述',
                                  validators=[Required(), Length(1, 64)],render_kw={"placeholder": u"请输入产品描述"})
    product_status = RadioField(u'产品状态',
                                choices=[('1', '正常'), ('0', '禁用')],
                                default='1')

    submit = SubmitField('提交')


class Add_Software(Form):
    product_name = StringField('产品名称',
                                validators=[Required(), Length(1, 64)],
                                render_kw={"placeholder": u"请输入产品名称"})
    product_descrit = StringField('产品描述',
                                validators=[Required(), Length(1, 64)],
                                render_kw={"placeholder": u"请输入产品描述"}
                                )
    product_status = RadioField('产品状态',
                                choices=[('1', '正常'), ('0', '禁用')],
                                default='1')
    version_name = StringField('版本名称',
                               validators=[Required(), Length(1, 64)],
                               render_kw={"placeholder": u"请输入版本名称"})
    version_descrit = StringField('版本描述',
                                  validators=[Required(), Length(1, 64)],
                                  render_kw={"placeholder": u"请输入版本描述"})
    software_version = StringField('软件版本列表', validators=[Required()],
                                    render_kw={"placeholder": u"请输入版本列表，以分号间隔"})
    version_features = StringField('软件特性列表', validators=[Required()],
                                    render_kw={"placeholder": u"请输入特性列表，以分号间隔"})
    submit = SubmitField('提交')


class Add_Version(Form):
    product_name = StringField('产品名称',
                                validators=[Required(), Length(1, 64)],
                                render_kw={"placeholder": u"请输入产品名称"})
    product_descrit = StringField('产品描述',
                                validators=[Required(), Length(1, 64)],
                                render_kw={"placeholder": u"请输入产品描述"}
                                )
    version_name = StringField('版本名称',
                               validators=[Required(), Length(1, 64)],
                               render_kw={"placeholder": u"请输入版本名称"})
    version_descrit = StringField('版本描述',
                                  validators=[Required(), Length(1, 64)],
                                  render_kw={"placeholder": u"请输入版本描述"})

    submit = SubmitField('提交')


class Add_Software2(Form):
    product_name = StringField('产品名称',
                                validators=[Required(), Length(1, 64)],
                                render_kw={"placeholder": u"请输入产品名称"})
    product_descrit = StringField('产品描述',
                                validators=[Required(), Length(1, 64)],
                                render_kw={"placeholder": u"请输入产品描述"}
                                )
    version_name = StringField('版本名称',
                               validators=[Required(), Length(1, 64)],
                               render_kw={"placeholder": u"请输入版本名称"})
    version_descrit = StringField('版本描述',
                                  validators=[Required(), Length(1, 64)],
                                  render_kw={"placeholder": u"请输入版本描述"})

    software_name = StringField('软件版本描述',
                                  validators=[Required(), Length(1, 64)],
                                  render_kw={"placeholder": u"请输入版本名称"})
    software_descrit = StringField('版本描述',
                                  validators=[Required(), Length(1, 64)],
                                  render_kw={"placeholder": u"请输入版本描述"})

    submit = SubmitField('提交')



class Add_Feature(Form):
    product_name = StringField('产品名称',
                                validators=[Required(), Length(1, 64)],
                                render_kw={"placeholder": u"请输入产品名称"})
    product_descrit = StringField('产品描述',
                                validators=[Required(), Length(1, 64)],
                                render_kw={"placeholder": u"请输入产品描述"}
                                )
    version_name = StringField('版本名称',
                               validators=[Required(), Length(1, 64)],
                               render_kw={"placeholder": u"请输入版本名称"})
    version_descrit = StringField('版本描述',
                                  validators=[Required(), Length(1, 64)],
                                  render_kw={"placeholder": u"请输入版本描述"})

    feature_name = StringField('软件版本描述',
                                  validators=[Required(), Length(1, 64)],
                                  render_kw={"placeholder": u"请输入版本名称"})
    feature_descrit = StringField('版本描述',
                                  validators=[Required(), Length(1, 64)],
                                  render_kw={"placeholder": u"请输入版本描述"})

    submit = SubmitField('提交')