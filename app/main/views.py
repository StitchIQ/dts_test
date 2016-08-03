# coding=utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from datetime import datetime
import logging
import bson.binary
from cStringIO import StringIO

from flask_sqlalchemy import get_debug_queries

from flask import render_template, redirect, request, url_for, flash, \
    current_app, jsonify, abort, send_from_directory, make_response, send_file
from flask_login import login_required, current_user
from wtforms_components import read_only
from werkzeug import secure_filename

from . import main
from .countrol_func import Bug_Num_Generate, output_csv_file
from .forms import StandardBug, BugsProcess, TestLeadEdit, DevelopEdit, \
    TestLeadEdit2, BugClose
from ..email import send_email
from ..models import Bugs, User, Process, BugStatus, Permission, \
    Bug_Now_Status, ProductInfo, VersionInfo, Attachment
from .. import db, mongodb

from ..decorators import bug_edit_check2




# flash :"success" "info" "danger"
# TODO 增加单元测试。
# TODO 附件的在bug中不同阶段分类
dts_log = logging.getLogger('DTS')


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            dts_log.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/')
@login_required
def index(product=None, version=None, software=None):
    # bugs_list = Bugs.query.filter_by(bug_owner=current_user).all()
    page = request.args.get('page', 1, type=int)
    product = request.args.get('product')
    version  = request.args.get('version')
    software = request.args.get('software')
    features = request.args.get('features')
    dts_log.debug(request.url)
    dts_log.debug(request.url_root)
    dts_log.debug(request.base_url)
    # sts=BugStatus.query.filter_by(id=6).first()
    # Bugs.bug_status not in [Bug_Now_Status.CREATED, Bug_Now_Status.CLOSED]
    # 不用的条件的查询结果 使用union，添加组合时，使用逗号分割，不要使用and
    a = Bugs.query.filter_by(bug_forbidden_status=False).filter(Bugs.bug_owner == current_user ,
                          Bugs.bug_status < Bug_Now_Status.CLOSED).filter(
                          Bugs.bug_status > Bug_Now_Status.CREATED)
    b = Bugs.query.filter_by(bug_forbidden_status=False).filter(Bugs.author == current_user ,
                          Bugs.bug_status == Bug_Now_Status.CREATED)

    a = a.union(b)
    if product:
        a = a.filter(Bugs.product_name == product)

    if version:
        a = a.filter(Bugs.product_version == version)

    if software:
        a = a.filter(Bugs.software_version == software)

    if features:
        a = a.filter(Bugs.version_features == features)

    pagination1 = a.order_by(Bugs.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    '''
    pagination1 = Bugs.query.filter(
            (Bugs.bug_owner == current_user and (Bug_Now_Status.CREATED < Bugs.bug_status and Bugs.bug_status< Bug_Now_Status.CLOSED)),
            (Bugs.author == current_user and Bugs.status_equal(Bug_Now_Status.CREATED))).order_by(
            Bugs.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    '''
    dts_log.debug("index")
    posts = pagination1.items
    return render_template('index.html',
                           bugs_list=posts, pagination=pagination1)


@main.route('/buglist')
@main.route('/buglist/<string:product>')
@login_required
def buglist(product=None):
    # bugs_list = Bugs.query.filter_by(bug_owner=current_user).all()
    page     = request.args.get('page', 1, type=int)
    version  = request.args.get('version')
    software = request.args.get('software')
    date     = request.args.get('date')
    features = request.args.get('features')
    serious  = request.args.get('serious')
    status   = request.args.get('status')
    author   = request.args.get('author')

    dts_log.debug(product)
    dts_log.debug(request.view_args)
    dts_log.debug(request.args)
    dts_log.debug(request.url)
    dts_log.debug(request.url_root)
    dts_log.debug(request.base_url)

    bugs_list = Bugs.query

    if product:
        bugs_list = bugs_list.filter(Bugs.product_name == product)

    if version:
        bugs_list = bugs_list.filter(Bugs.product_version == version)

    if software:
        bugs_list = bugs_list.filter(Bugs.software_version == software)

    if date:
        bugs_list = bugs_list.filter(db.func.date(Bugs.timestamp)== date)

    if features:
        bugs_list = bugs_list.filter(Bugs.version_features == features)

    if serious:
        bugs_list = bugs_list.filter(Bugs.bug_level == serious)

    if status:
        st = BugStatus.query.filter_by(bug_status_descrit=status).first()
        bugs_list = bugs_list.filter_by(now_status = st)

    if author:
        au = User.query.filter_by(username=author).first()
        bugs_list = bugs_list.filter_by(author = au)

    pagination = bugs_list.order_by(Bugs.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    items = pagination.items
    dts_log.debug(buglist.__name__)
    return render_template('index.html', bugs_list=items, pagination=pagination)


@main.route('/check_user')
@login_required
def check_user():
    email = request.args.get('username', 0, type=str)
    status = User.get_by_email(email)
    if status:
        return status.username
    else:
        return 'Not Found', 200


@main.route('/get_product')
@login_required
def get_product():
    product_info = ProductInfo.get_all_product()
    return jsonify({
        'product_info': [post.product_name_json() for post in product_info]
        })


@main.route('/get_software')
@login_required
def get_software():
    # jquery传递的参数需要转码
    product_name = unicode(request.args.get('product', 0, type=str))
    # software = VersionInfo.query.filter_by(product_name=a)
    version = VersionInfo.get_by_product(product_name)

    # 对于外键，在连接时还是要使用原来的值
    # print str(VersionInfo.query.join(ProductInfo,
    # ProductInfo.id==VersionInfo.product).filter(
    #            ProductInfo.product_name==a))

    return jsonify({
        'soft_info': [v.software_to_json() for v in version]
        })


@main.route('/task')
@main.route('/task/<string:mytask>')
@main.route('/task/<string:mytask>/<string:product>')
@main.route('/task/<string:mytask>/<string:product>/<string:version>')
@main.route('/task/<string:mytask>/<string:product>/<string:version>/<string:software>')
@login_required
def task(mytask='process', product=None, version=None, software=None):
    dts_log.debug(request.url)
    dts_log.debug(request.url_root)
    dts_log.debug(request.view_args)
    dts_log.debug(request.base_url)
    dts_log.debug(request.endpoint)
    dts_log.debug(request.view_args.copy())
    page = request.args.get('page', 1, type=int)
    dts_log.debug(mytask)
    if mytask == 'process':
        a = Bugs.query.filter(Bugs.bug_owner == current_user ,
                              Bugs.bug_status < Bug_Now_Status.CLOSED).filter(
                              Bugs.bug_status > Bug_Now_Status.CREATED)
        b = Bugs.query.filter(Bugs.author == current_user ,
                              Bugs.bug_status == Bug_Now_Status.CREATED)

        pagination = a.union(b)


    if mytask == 'created':

        pagination = Bugs.query.filter_by(author=current_user)
        # posts = pagination2.items

    if mytask == 'processed':

        # 查询的思路是表连接,要去重复值
        pagination = Bugs.query.join(
                    Process,
                    Process.bugs_id == Bugs.bug_id).distinct().filter(
                    Process.operator == current_user)

    if product:
        pagination = pagination.filter(Bugs.product_name == product)

    if version:
        pagination = pagination.filter(Bugs.product_version == version)

    if software:
        pagination = pagination.filter(Bugs.software_version == software)

    pagination = pagination.order_by(Bugs.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)

    posts = pagination.items
    # flash(str(Bugs.query.join(Process, Process.bugs_id == Bugs.bug_id).filter(
    #        Process.operator == current_user)))
    return render_template('main.html', bugs_list=posts,
                           pagination=pagination, mytask=mytask)


@main.route('/copy_to_me/')
@login_required
def copy_to_me():
    # TODO 待实现抄送功能
    page = request.args.get('page', 1, type=int)
    # sts=BugStatus.query.filter_by(id=6).first()

    pagination1 = Bugs.query.filter(
            Bugs.bug_owner == current_user,
            Bugs.bug_status < Bug_Now_Status.CLOSED).order_by(
            Bugs.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)

    posts = pagination1.items
    return render_template('index.html', bugs_list=posts,
                           pagination=pagination1)


@main.route('/newbugs', methods=['GET', 'POST'])
@login_required
def newbug():
    # TODO 此处有bug，当提交失败时，bug_id会变化，导致添加的附件无法关联到bug
    form = StandardBug()
    if request.method == 'GET':
        form.bugs_id.data = Bug_Num_Generate.bug_num()

    read_only(form.bugs_id)

    dts_log.debug(form.errors)
    dts_log.debug(form.validate_on_submit())

    # print request.values
    if form.validate_on_submit():
        if request.form.get('submit'):
            form.bug_status.data = Bug_Now_Status.TESTLEADER_AUDIT

        if request.form.get('save_crft'):
            form.bug_status.data = Bug_Now_Status.CREATED
        # if request.method == 'POST':
        #print form.version_features.value

        if len(form.errors) != 0:
            return render_template("standard_bug.html", form=form)

        f = request.files['attachment']
        fname = None
        is_has_attach_files = False

        if f.filename != '':
            # fname = UPLOAD_FOLDER + secure_filename(f.filename)
            # f.save(app_dir + UPLOAD_FOLDER + secure_filename(f.filename))
            is_has_attach_files = True

        dts_log.debug(unicode(form.version_features.data))
        bug = Bugs(bug_id=form.bugs_id.data,
                   product_name=unicode(form.product_name.data),
                   product_version=unicode(form.product_version.data),
                   software_version=unicode(form.software_version.data),
                   version_features=unicode(form.version_features.data),
                   bug_level=form.bug_level.data,
                   bug_insiders=form.bug_insiders.data,
                   bug_show_times=form.bug_show_times.data,
                   bug_title=form.bug_title.data,
                   bug_descrit=form.bug_descrit.data,
                   bug_owner=User.query.filter_by(
                                        email=form.bug_owner_id.data).first(),
                   author=current_user._get_current_object(),
                   bug_status=form.bug_status.data,
                   bug_photos=fname,
                   bug_attachments=is_has_attach_files)

        db.session.add(bug)

        process = Process(operator=current_user._get_current_object(),
                          author=User.query.filter_by(
                          email=form.bug_owner_id.data).first(),
                          bugs=bug,
                          old_status=Bug_Now_Status.CREATED,
                          new_status=form.bug_status.data,
                          opinion='')
        db.session.add(process)
        db.session.commit()

        flash(u'Bugs 提交成功.', "success")
        return redirect(url_for('.bug_process', id=bug.bug_id))

    form.bug_descrit.data = u'''
支持MarkDown语法，帮助查看

问题单填写规范：
### 环境信息
*详细描述测试时的环境信息*

### 操作步骤

1. 打开页面
2. 输入参数

### 预期结果

1. 看到视频
2. 参数显示

### 实际结果

1. 看到乱码
'''
    return render_template("standard_bug.html", form=form)


@main.route('/upload', methods=['POST'])
@login_required
def upload():
    import mimetypes
    from tempfile import mktemp
    from werkzeug.utils import secure_filename

    ALLOWED_MIMETYPES = {'image/jpg', 'image/jpeg', 'image/png', 'image/gif',
                         'image/pjpeg', 'image/x-png'}

    if request.method == 'GET':
        return render_template('upload.html', img='')

    bug_id = None
    uploadedFile = None
    try:
        bug_id = request.form.get('bugs_id')
        uploadedFile = request.files['attachment']
        if not uploadedFile or not bug_id:
            return abort(400)
    except:
        return abort(400)

    #mongo_id = save_file(bug_id, uploadedFile)
    pasteFile = Attachment.create_by_uploadFile(bug_id, uploadedFile)
    #db.session.add(pasteFile)
    #db.session.commit()

    return jsonify({
            "symlink": pasteFile.symlink,
            "filename": pasteFile.filename})


@main.route('/viewimage/<symlink>')
def viewimage(symlink=None):
    pasteFile = Attachment.get_by_symlink(symlink)

    if not pasteFile:
        return abort(404)

    #return redirect(pasteFile.url_p)
    if  not current_app.config['MONGO_DB_USE']:
        response = make_response(send_from_directory(current_app.config['UPLOAD_FOLDER'], pasteFile.filehash))
        return response
    try:
        f = mongodb.files.find_one({"symlink":symlink})
        dts_log.debug(f['filename'])
        if f is None:
            dts_log.error(''.join([symlink, ' 没有找到']))
            raise bson.errors.InvalidId()
        #response = make_response(f['content'],mimetype='image/' + f['mime'])
        #response.headers['Content-Disposition'] = "attachment; filename={}".format("a.jpg")
        #return response
        response = make_response(send_file(StringIO(f['content'])))
        response.headers['Content-Type'] = f['mimetype']
        return response
    except bson.errors.InvalidId:
        abort(404)


@main.route('/viewlargeimage/<symlink>')
def viewlargeimage(symlink=None):
    return render_template('imageview.html', symlink=symlink)


@main.route('/delete/<symlink>', methods=['GET', 'POST'])
@login_required
def delete_file(symlink):
    """ 管理员页面附件删除也调用了此函数 """
    pasteFile = Attachment.get_by_symlink(symlink)
    if not pasteFile:
        return abort(404)

    bugs = Bugs.query.filter_by(bug_id=pasteFile.bug_id).first()
    # 检查是否有删除附件的权限
    if bugs:
        if not (current_user == bugs.author and \
                bugs.status_equal(Bug_Now_Status.CREATED)) and \
                not current_user.can(Permission.ADMINISTER):
            dts_log.error(''.join([current_user,' can not operate : ', bugs.bug_id]))
            return abort(403)

    if pasteFile.file_delete(symlink):
        return jsonify({
                    "delete": 'OK' ,
                    "id": pasteFile.symlink})
    else:
        return abort(404)


@main.route('/download/<filehash>')
@login_required
def download_file(filehash):
    downloadFile = Attachment.get_by_filehash(filehash)

    if not downloadFile:
        return abort(404)

    response = make_response(send_from_directory(current_app.config['UPLOAD_FOLDER'], downloadFile.filehash))
    response.headers['Content-Disposition'] = "attachment; filename={}".format(downloadFile.filename)

    return response

@main.route('/down/<symlink>')
@login_required
def download(symlink):
    downloadFile = Attachment.get_by_symlink(symlink)
    if not downloadFile:
        dts_log.error(''.join([symlink, ' 没有找到']))
        return abort(404)

    response = make_response()

    if current_app.config['MONGO_DB_USE']:
        dts_log.debug(''.join([symlink, ' 使用mongodb']))
        f = mongodb.files.find_one({"symlink":symlink})
        if f is None:
            dts_log.error(''.join([symlink, ' 没有找到']))
            return abort(404)
        response = make_response(send_file(StringIO(f['content'])))
        # print response.headers['Content-Disposition']
        response.headers['Content-Disposition'] = "attachment; filename={}".format(downloadFile.filename)
        response.headers['Content-Type'] = "application/octet-stream"
    else:
        response = make_response(send_from_directory(current_app.config['UPLOAD_FOLDER'], downloadFile.filehash))
        # 使用X-Accel-Redirect可以隐藏文件下载地址
        response.headers['X-Accel-Redirect'] = redirect(url_for('.download_file', filehash=downloadFile.filehash))
        response.headers['Content-Disposition'] = "attachment; filename={}".format(downloadFile.filename)
        response.headers['Content-Type'] = "application/octet-stream"

    return response


@main.route('/bug_process/<string:id>', methods=['GET', 'POST'])
@login_required
def bug_process(id):
    # TODO 需要在页面上显示问题的解决版本和回归测试版本
    bugs = Bugs.get_by_bug_id(id)
    attachments = Attachment.query.filter_by(bug_id=id).all()

    form = BugsProcess()
    testleadedit = TestLeadEdit()
    developedit = DevelopEdit()
    testleadedit2 = TestLeadEdit2()
    bugclose = BugClose()


    if bugs.bug_status == Bug_Now_Status.TESTLEADER_AUDIT \
            and current_user == bugs.bug_owner:
        dts_log.debug('testleaderedit test')
        if testleadedit.validate_on_submit():
            dts_log.debug('testleaderedit')
            dts_log.debug(testleadedit.bug_status.data)
            dts_log.debug(developedit.bug_status.data)
            bugs.bug_owner_id = User.get_by_email(
                                    testleadedit.bug_owner_id.data).id

            process = Process(operator=current_user._get_current_object(),
                              author=User.query.filter_by(
                              email=testleadedit.bug_owner_id.data).first(),
                              bugs=bugs,
                              old_status=bugs.bug_status,
                              new_status=testleadedit.bug_status.data,
                              opinion=testleadedit.test_process_opinion.data)
            bugs.ping()
            db.session.add(process)

            bugs.bug_status = testleadedit.bug_status.data
            db.session.add(bugs)
            db.session.commit()

            # flash(process_list.timestamp)
            flash('测试经理更新成功.', "success")

            return redirect(url_for('.bug_process', id=bugs.bug_id))

    if developedit.validate_on_submit() and current_user == bugs.bug_owner \
            and bugs.bug_status == Bug_Now_Status.DEVELOPMENT:
        dts_log.debug('developedit')
        dts_log.debug(testleadedit.bug_owner_id.data)
        bugs.bug_owner_id = User.query.filter_by(
            email=developedit.bug_owner_id.data).first().id
        process = Process(operator=current_user._get_current_object(),
                          author=User.query.filter_by(
                          email=developedit.bug_owner_id.data).first(),
                          bugs=bugs,
                          old_status=bugs.bug_status,
                          new_status=developedit.bug_status.data,
                          opinion=developedit.deve_process_opinion.data)
        bugs.ping()
        db.session.add(process)

        bugs.bug_status = developedit.bug_status.data
        bugs.resolve_version = developedit.dresolve_version.data
        bugs.version_features = developedit.dversion_features.data
        db.session.add(bugs)
        db.session.commit()
        flash('开发人员更新成功.', "success")

        return redirect(url_for('.bug_process', id=bugs.bug_id))

    if testleadedit2.validate_on_submit() and current_user == bugs.bug_owner \
            and bugs.bug_status == Bug_Now_Status.TESTLEADER_REGESSION:
        dts_log.debug('testleadedit2')
        bugs.bug_owner_id = User.query.filter_by(
            email=testleadedit2.bug_owner_id.data).first().id

        process = Process(operator=current_user._get_current_object(),
                          author=User.query.filter_by(
                          email=testleadedit2.bug_owner_id.data).first(),
                          bugs=bugs,
                          old_status=bugs.bug_status,
                          new_status=testleadedit2.bug_status.data,
                          opinion=testleadedit2.process_opinion.data)
        db.session.add(process)

        bugs.bug_status = testleadedit2.bug_status.data
        db.session.add(bugs)
        db.session.commit()
        flash('测试经理更新成功.', "success")

        return redirect(url_for('.bug_process', id=bugs.bug_id))

    if bugclose.validate_on_submit() and current_user == bugs.bug_owner \
            and bugs.bug_status == Bug_Now_Status.REGRESSION_TESTING:
        if str(bugclose.bug_status.data) == str(Bug_Now_Status.TESTLEADER_REGESSION):
            bugs.bug_owner_id = User.query.filter_by(
                email=bugclose.bug_owner_id.data).first().id
            process = Process(operator=current_user._get_current_object(),
                              author=User.query.filter_by(
                              email=testleadedit2.bug_owner_id.data).first(),
                              bugs=bugs,
                              old_status=bugs.bug_status,
                              new_status=bugclose.bug_status.data,
                              opinion=bugclose.process_opinion.data)

        else:
            bugs.bug_owner_id = None
            process = Process(operator=current_user._get_current_object(),
                              author=None,
                              bugs=bugs,
                              old_status=bugs.bug_status,
                              new_status=bugclose.bug_status.data,
                              opinion=bugclose.process_opinion.data)
        db.session.add(process)

        bugs.bug_status = bugclose.bug_status.data
        bugs.regression_test_version = bugclose.regression_test_version.data
        db.session.add(bugs)
        db.session.commit()
        flash('测试人员更新成功.', "success")
        return redirect(url_for('.bug_process', id=bugs.bug_id))

    # 处理日志
    process_log = bugs.process.order_by(Process.timestamp.asc())
    testmanager_log = bugs.process.filter_by(
                        old_status=Bug_Now_Status.TESTLEADER_AUDIT).order_by(
                        Process.timestamp.desc())
    developedit_log = bugs.process.filter_by(
                        old_status=Bug_Now_Status.DEVELOPMENT).order_by(
                        Process.timestamp.desc())
    bugtest_log = bugs.process.filter_by(
                    old_status=Bug_Now_Status.TESTLEADER_REGESSION).order_by(
                    Process.timestamp.desc())
    retest_log = bugs.process.filter_by(
                        old_status=Bug_Now_Status.REGRESSION_TESTING).order_by(
                        Process.timestamp.desc())
    # post.comments.order_by(Comment.timestamp.asc()) .filter_by(status='3')

    software_version = VersionInfo.query.join(
            ProductInfo,
            ProductInfo.id == VersionInfo.product).filter(
            ProductInfo.product_name == bugs.product_name,
            bugs.product_version == VersionInfo.version_name).first()
    # 设置selectfield的默认值，使用.data直接赋值，即可
    developedit.dresolve_version.choices = [('-1', u'--请选择 软件版本--')] + \
        software_version.software_to_turple()
    developedit.dresolve_version.data = bugs.software_version

    developedit.dversion_features.choices = [('-1', u'--请选择 软件特性--')] +\
        software_version.features_to_turple()
    developedit.dversion_features.data = bugs.version_features

    bugclose.regression_test_version.choices =  \
        [('-1', u'--请选择 软件版本--')] + software_version.software_to_turple()
    bugclose.regression_test_version.data = bugs.resolve_version
    bugclose.bug_owner_id.data = process_log[-1].operator.email
    #flash(process_log[-1].author.email)

    form.bugs_id.data = bugs.bug_id
    form.product_name.data = bugs.product_name
    form.product_version.data = bugs.product_version
    form.software_version.data = bugs.software_version
    form.version_features.data = bugs.version_features
    form.bug_level.data = bugs.bug_level
    form.bug_insiders.data = bugs.bug_insiders
    form.bug_show_times.data = bugs.bug_show_times
    bug_descrit_html = bugs.bug_descrit_html
    form.bug_title.data = bugs.bug_title

    read_only(form.bugs_id)
    read_only(form.bug_title)
    read_only(form.product_name)
    read_only(form.product_version)
    read_only(form.software_version)
    read_only(form.version_features)
    read_only(form.bug_level)
    read_only(form.bug_insiders)
    read_only(form.bug_show_times)
    read_only(form.bug_descrit)

    # flash(process_list.first().opinion)

    return render_template('bugs_process.html',
                           form=form, bugs=bugs, attachments=attachments,
                           testleadedit=testleadedit, developedit=developedit,
                           testleadedit2=testleadedit2, bugclose=bugclose,
                           testmanager_log=testmanager_log,
                           process_log=process_log,
                           developedit_log=developedit_log,
                           bugtest_log=bugtest_log,
                           retest_log=retest_log,
                           bug_descrit_html=bug_descrit_html)


@main.route('/bug_edit/<string:bug_id>', methods=['GET', 'POST'])
@login_required
def bug_edit(bug_id):
    dts_log.debug(bug_id)
    bugs = Bugs.get_by_bug_id(bug_id)
    # 检查是否编辑权限
    if not (current_user == bugs.author and \
            bugs.status_equal(Bug_Now_Status.CREATED)) and \
            not current_user.can(Permission.ADMINISTER):
        return render_template('404.html'), 404

    attachments = None
    if bugs.bug_attachments:
        attachments = Attachment.get_all_attach_by_bug_id(bug_id)

    process_log = bugs.process.order_by(Process.timestamp.asc())

    form = StandardBug()

    if form.validate_on_submit():
        # 判断是提交还是保存草稿
        if request.form.get('submit'):
            form.bug_status.data = Bug_Now_Status.TESTLEADER_AUDIT
        if request.form.get('save_crft'):
            form.bug_status.data = bugs.bug_status

        bugs.product_name = form.product_name.data
        bugs.product_version = form.product_version.data
        bugs.software_version = form.software_version.data
        bugs.version_features = form.version_features.data
        bugs.bug_level = form.bug_level.data
        bugs.bug_insiders = form.bug_insiders.data
        bugs.bug_show_times = form.bug_show_times.data
        bugs.bug_title = form.bug_title.data
        bugs.bug_descrit = form.bug_descrit.data
        bugs.bug_owner = User.query.filter_by(
                            email=form.bug_owner_id.data).first()
        bugs.author = current_user._get_current_object()
        bugs.bug_status = form.bug_status.data
        bugs.bug_photos = None
        db.session.add(bugs)

        # bug_owner_id=form.bug_owner_id.data,
        # bug.timestamp = db.Column(db.DateTime,
        # index=True, default=datetime.utcnow)
        process = Process(operator=current_user._get_current_object(),
                          author=User.query.filter_by(
                          email=form.bug_owner_id.data).first(),
                          bugs=bugs,
                          old_status='1',
                          new_status=form.bug_status.data,
                          opinion='')
        db.session.add(process)
        db.session.commit()
        flash('Bugs 提交成功.', "success")
        return redirect(url_for('.bug_process', id=bugs.bug_id))


    product_info = ProductInfo.query.filter_by(product_status=True).all()
    form.product_name.choices = [('-1', u'--请选择 产品名称--')] + \
        [post.product_name_turple() for post in product_info]
    form.product_name.selected = bugs.product_name

    # 初始化selectfiled,默认值设置为原来bug的值
    # 设置selectedfield的默认值，直接使用.data属性即可
    product_version = VersionInfo.query.join(
            ProductInfo,
            ProductInfo.id == VersionInfo.product).filter(
            ProductInfo.product_name == bugs.product_name).all()

    form.product_version.choices = [('-1', u'--请选择 产品版本--')] + \
        [s.version_to_turple() for s in product_version]
    # form.product_version.selected = bugs.product_version

    software_version = VersionInfo.query.join(
                ProductInfo,
                ProductInfo.id == VersionInfo.product).filter(
                ProductInfo.product_name == bugs.product_name,
                bugs.product_version == VersionInfo.version_name).first()

    form.software_version.choices = [('-1', u'--请选择 软件版本--')] + \
        software_version.software_to_turple()
    # form.software_version.selected = bugs.software_version

    form.version_features.choices = [('-1', u'--sss--')] + \
        software_version.features_to_turple()
    # form.version_features.selected = bugs.version_features

    form.bugs_id.data = bugs.bug_id
    form.product_name.data = bugs.product_name
    form.product_version.data = bugs.product_version
    form.software_version.data = bugs.software_version
    form.version_features.data = bugs.version_features
    form.bug_level.data = bugs.bug_level
    form.bug_insiders.data = bugs.bug_insiders
    form.bug_show_times.data = bugs.bug_show_times
    form.bug_descrit.data = bugs.bug_descrit
    form.bug_title.data = bugs.bug_title
    form.bug_owner_id.data = bugs.bug_owner.email
    # form.photo.data = bugs.bug_photos
    # flash(process_list.first().opinion)
    read_only(form.bugs_id)
    return render_template('bug_edit.html', form=form, attachments=attachments,
                           bugs=bugs, process_log=process_log)


@main.route('/test')
@login_required
def test2():
    print request.args.get('search')
    #return render_template('autocomplate.html')
    return render_template('test/checkbox.html')


@main.route('/autocomplete', methods=['GET'])
@login_required
def get_user():
    search = request.args.get('query', 0, type=str)
    dts_log.debug(search.isalnum())
    if not search.isalnum():
        return 'Not Found', 200
    user = User.query.filter(User.email.like(search + '%')).all()
    return jsonify({"suggestions":[u.email for u in user]})


@main.route('/daochu', methods=['POST'])
@login_required
def daochu():
    bug_list = request.json

    return jsonify({'filename':output_csv_file(bug_list)})


@main.route('/daochu2/<filename>')
@login_required
def data_output(filename):
    response = make_response(send_from_directory(current_app.config['OUTPUT_FOLDER'], filename))
    response.headers['Content-Disposition'] = "attachment; filename={}".format(filename)
    response.headers['Cache-Control'] = "no-cache, no-store, max-age=0, must-revalidate"
    return response
