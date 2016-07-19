# coding=utf-8
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, RadioField, \
        SelectField, IntegerField
from wtforms.validators import Required, Length, Email
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from flask_wtf.file import FileField, FileAllowed

from ..models import ProductInfo


class MySelectField(SelectField):
    # 重写验证函数，只要值不为-1，就通过
    def pre_validate(self, form):
        if str(self.data) == '-1':
            raise ValueError(self.gettext(u'请选择'))


class StandardBug(Form):
    bugs_id = StringField(u'问题单号')
    product_name = MySelectField(u'产品名称', coerce=str, choices=[])
    product_version = MySelectField(u'产品版本号', coerce=str, choices=[])
    software_version = MySelectField(u'软件版本号', coerce=str, choices=[])
    version_features = MySelectField(u'软件特性', coerce=str, choices=[])
    bug_level = SelectField(u'严重程度',
                            choices=[(u'致命', u'致命'), (u'严重', u'严重'),
                                     (u'一般', u'一般'), (u'提示', u'提示')])
    system_view = StringField(u'问题单知情人')
    bug_show_times = SelectField(u'出现频率',
                                 choices=[(u'必现', u'必现'),
                                          (u'频繁出现', u'频繁出现'),
                                          (u'概率出现', u'概率出现'),
                                          (u'较难重现', u'较难重现'),
                                          (u'无法重现', u'无法重现')])
    bug_title = StringField(u'问题标题', validators=[Required(), Length(1, 100)],render_kw={"placeholder": u"概述描述问题单情况，长度不超过100字符"})
    bug_descrit = PageDownField(u'问题描述', validators=[Required()], render_kw={"placeholder": "支持MarkDown语法，帮助查看：http://www.jianshu.com/p/1e402922ee32/"})
    bug_owner_id = StringField(u'问题处理人', validators=[Required(), Email()],render_kw={"placeholder": u"请输入处理人邮箱地址"})
    bug_status = RadioField(u'选择处理',
                            choices=[('1', u'新建'),
                                     ('2', u'测试经理审核')], default='2')
    # save = SubmitField('保存')
    attachment = FileField(u'附件')
    save_crft = SubmitField(u'保存草稿')
    submit = SubmitField(u'提交')

    def __init__(self):
        super(StandardBug, self).__init__()
        product_info = ProductInfo.get_all_product()
        self.product_name.choices = [('-1', u'请选择产品')] + [
                        post.product_name_turple() for post in product_info]

        self.product_version.choices  = [('-1', u'请选择产品版本')]
        self.software_version.choices = [('-1', u'请选择软件版本')]
        self.version_features.choices = [('-1', u'请选择软件特性')]



    # 自定义的验证函数
    def validate_product_name(self, field):
        if str(field.data) == '-1':
            raise ValidationError("Not a valid choice")


class BugsProcess(Form):
    bugs_id = StringField(u'问题单号')
    product_name = StringField(u'产品名称')
    product_version = StringField(u'产品版本号')
    software_version = StringField(u'软件版本号')
    version_features = StringField(u'软件特性')
    bug_level = StringField(u'严重程度')
    system_view = StringField(u'系统表现')
    bug_show_times = StringField(u'出现频率')
    bug_title = StringField(u'问题标题')
    bug_descrit = TextAreaField(u'问题描述')
    # bug_owner_id = StringField('问题处理人')


class TestLeadEdit(Form):
    test_process_opinion = TextAreaField(u'处理意见', validators=[Required()])
    bug_owner_id = StringField(u'问题单处理人', validators=[Required(), Email()],render_kw={"placeholder": u"请输入处理人邮箱地址"})
    bug_status = RadioField(u'选择处理',
                            choices=[('1', u'返回修改'), ('3', u'开发人员修改')],
                            default='3')
    submit = SubmitField(u'提交')



class DevelopEdit(Form):
    dresolve_version = MySelectField('解决版本',  coerce=str, choices=[])
    dversion_features = MySelectField('软件特性', coerce=str, choices=[])
    deve_process_opinion = TextAreaField('处理意见', validators=[Required()])
    bug_owner_id = StringField('问题单处理人', validators=[Required(), Email()],render_kw={"placeholder": u"请输入处理人邮箱地址"})
    bug_status = RadioField('选择处理',
                            choices=[('2', '返回测试经理'),
                                     ('3', '转交其他开发人员处理'),
                                     ('4', '测试经理组织回归测试')],
                            default='4', validators=[Required()])
    submit = SubmitField('提交')


class TestLeadEdit2(Form):
    process_opinion = TextAreaField('处理意见', validators=[Required()])
    bug_owner_id = StringField('问题单处理人',
                               validators=[Required(), Email()],render_kw={"placeholder": u"请输入处理人邮箱地址"})
    bug_status = RadioField('选择处理',
                            choices=[('3', '返回开发人员修改'),
                                     ('5', '测试人员回归')], default='5')
    submit = SubmitField('提交')


class BugClose(Form):
    regression_test_version = MySelectField('回归测试版本',
                                            coerce=str, choices=[])
    process_opinion = TextAreaField('处理意见', validators=[Required()])
    bug_owner_id = StringField('问题单处理人', validators=[Required(), Email()])
    bug_status = RadioField('选择处理',
                            choices=[('6', '问题关闭'),
                                     ('4', '测试经理组织回归测试')],
                            default='6')
    submit = SubmitField('提交')
