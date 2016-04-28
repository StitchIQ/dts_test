# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from datetime import datetime

from flask import render_template, redirect, request, url_for, flash, \
    current_app, jsonify, abort, send_from_directory
from flask.ext.login import login_required, current_user
from wtforms_components import read_only
from werkzeug import secure_filename

from . import main
from .countrol_func import Bug_Num_Generate
from .forms import StandardBug, BugsProcess, TestLeadEdit, DevelopEdit, \
    TestLeadEdit2, BugClose
from ..email import send_email
from ..models import Bugs, User, Process, BugStatus, Permission, \
    Bug_Now_Status, ProductInfo, VersionInfo, Attachment
from .. import db

@main.route('/')
@login_required
def index():
    # bugs_list = Bugs.query.filter_by(bug_owner=current_user).all()

    page = request.args.get('page', 1, type=int)
    # sts=BugStatus.query.filter_by(id=6).first()
    # Bugs.bug_status not in [Bug_Now_Status.CREATED, Bug_Now_Status.CLOSED]
    # 不用的条件的查询结果 使用union，添加组合时，使用逗号分割，不要使用and
    a = Bugs.query.filter(Bugs.bug_owner == current_user ,
                          Bugs.bug_status < Bug_Now_Status.CLOSED).filter(
                          Bugs.bug_status > Bug_Now_Status.CREATED)
    b = Bugs.query.filter(Bugs.author == current_user ,
                          Bugs.bug_status == Bug_Now_Status.CREATED)

    pagination1 = a.union(b).order_by(Bugs.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    '''
    pagination1 = Bugs.query.filter(
            (Bugs.bug_owner == current_user and (Bug_Now_Status.CREATED < Bugs.bug_status and Bugs.bug_status< Bug_Now_Status.CLOSED)),
            (Bugs.author == current_user and Bugs.status_equal(Bug_Now_Status.CREATED))).order_by(
            Bugs.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    '''

    posts = pagination1.items
    return render_template('index.html',
                           bugs_list=posts, pagination=pagination1)


@main.route('/check_user')
@login_required
def check_user():
    a = request.args.get('username', 0, type=str)
    status = User.query.filter_by(email=a).first()
    if status:
        return status.username
    else:
        return 'Not Found', 200


@main.route('/get_product')
@login_required
def get_product():
    product_info = ProductInfo.query.filter_by(product_status=True).all()

    return jsonify({
        'product_info': [post.product_name_json() for post in product_info]
        })
    # return '''[{"name": "NVR"},{"name": "IPC"}]'''
    # return '''[{id:"1",name:"pro001"},{id:"1",name:"pro002"}]'''


@main.route('/get_software')
@login_required
def get_software():
    a = request.args.get('product', 0, type=str)
    # software = VersionInfo.query.filter_by(product_name=a)
    # print 'sssss:',a
    software = VersionInfo.query.join(
               ProductInfo, ProductInfo.id == VersionInfo.product).filter(
               ProductInfo.product_name == a).all()

    # 对于外键，在连接时还是要使用原来的值
    # print str(VersionInfo.query.join(ProductInfo,
    # ProductInfo.id==VersionInfo.product).filter(
    #            ProductInfo.product_name==a))

    return jsonify({
        'soft_info': [soft.software_to_json() for soft in software]
        })
    # return jsonify({
    #    'product_info': [post.product_name_json() for post in product_info]
    #    })  [{id:"1",name:"amdin"},{id:"1",name:"amdin"}]
    # return '''[{"name": "V100"},{"name": "V200"}]'''
    # return '''[{id:"1",name:"soft001"},{id:"1",name:"soft002"}]'''


@main.route('/get_version')
@login_required
def get_version():
    a = request.args.get('version', 0, type=str)
    version = VersionInfo.query.filter_by(version_name=a).all()
    print 'DDDDD::', len(version)
    # return jsonify({
    #    'product_info': [post.product_name_json() for post in product_info]
    #    })
    # return '''['B101','B020','B030']'''
    return '''[{"name": "B010"},{"name": "B020"}]'''
    # return '''[{id:"1",name:"ver001"},{id:"1",name:"ver002"}]'''


@main.route('/_add_numbers')
@login_required
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@main.route('/add')
@login_required
def add_numbers2():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return '''[
    {
        "product_name": "NVR",
        "version_list": [
            {
                "product_verison": "V100",
                "soft_version": [
                    "B101",
                    "B102"
                ]
            },
            {
                "product_verison": "V222",
                "soft_version": [
                    "B201",
                    "B202"
                ]
            }
        ]
    },
    {
        "product_name": "IPC",
        "version_list": [
            {
                "product_verison": "V300",
                "soft_version": [
                    "B111",
                    "B121"
                ]
            }
        ]
    }
]'''


@main.route('/jsontable')
@login_required
def jsontable():
    # http://blog.csdn.net/porschev/article/details/5943579
    # pageIndex=1&pageSize=20
    # page = request.args.get('page', 1, type=int)
    # sts=BugStatus.query.filter_by(id=6).first()
    page = request.args.get('pageIndex', 1, type=int)
    size = request.args.get('pageSize', 1, type=int)
    pagination1 = Bugs.query.filter(
            Bugs.bug_owner == current_user,
            Bugs.bug_status < Bug_Now_Status.CLOSED).order_by(
            Bugs.timestamp.desc()).paginate(
            page, per_page=size,
            error_out=False)

    posts = pagination1.items
    flash(posts)
    return render_template('table_list2.html')


@main.route('/datatable')
@login_required
def datatable():

    return render_template('datatable.html')


@main.route('/myjson')
@login_required
def myjson():
    # page = request.args.get('page', 1, type=int)
    page = request.args.get('pageIndex', 1, type=int)
    size = request.args.get('pageSize', 1, type=int)

    pagination = Bugs.query.filter(
            Bugs.bug_owner == current_user,
            Bugs.bug_status < Bug_Now_Status.CLOSED).order_by(
            Bugs.timestamp.desc()).paginate(
            page, per_page=size,
            error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('main.myjson', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('main.myjson', page=page+1, _external=True)

    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total,
        'pages': pagination.pages
        })


@main.route('/myjson2')
@login_required
def myjson2():
    page = request.args.get('page', 1, type=int)

    pagination = Bugs.query.filter(
            Bugs.bug_owner == current_user,
            Bugs.bug_status < Bug_Now_Status.CLOSED).order_by(
            Bugs.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('main.myjson', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('main.myjson', page=page+1, _external=True)

    # query = Bugs.query
    query = db.session.query(Bugs).filter(
            Bugs.bug_owner == current_user,
            Bugs.bug_status < Bug_Now_Status.CLOSED).order_by(
            Bugs.timestamp.desc())
    # q = query.all()
    from datatables import DataTable
    rq = request.args
    # ('bugs_owner','bug_owner.username'),
    table = DataTable(request.args, Bugs, query, [
        "id",
        ('user_name', 'author_id'),
        "bug_level",
        ("bug_owner_id", 'bug_owner.username'),
        "bug_show_times",
        ('bug_status', 'now_status.bug_status_descrit'),
        "bug_title",
        "product_name",
        "product_version",
        "software_version",
        "system_view",
        "timestamp"
    ])

    return jsonify({
        'data': [post.to_json() for post in posts],
        "draw": 1,
        "recordsFiltered": pagination.total,
        "recordsTotal": pagination.total
        })

    # return jsonify(table.json())


@main.route('/task/<string:mytask>')
@login_required
def task(mytask):
    if mytask == 'created':
        page = request.args.get('page', 1, type=int)

        pagination = Bugs.query.filter_by(author=current_user).paginate(
                page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)
        # posts = pagination2.items

    if mytask == 'processed':
        page = request.args.get('page', 1, type=int)

        # 查询的思路是表连接,要去重复值
        pagination = Bugs.query.join(
                    Process,
                    Process.bugs_id == Bugs.bug_id).distinct().filter(
                    Process.operator == current_user).paginate(
                    page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out=False)

    posts = pagination.items
    # flash(str(Bugs.query.join(Process, Process.bugs_id == Bugs.bug_id).filter(
    #        Process.operator == current_user)))
    return render_template('main.html', bugs_list=posts,
                           pagination=pagination, mytask=mytask)


@main.route('/copy_to_me/')
@login_required
def copy_to_me():
    page = request.args.get('page', 1, type=int)
    # sts=BugStatus.query.filter_by(id=6).first()

    pagination1 = Bugs.query.filter(
            Bugs.bug_owner == current_user,
            Bugs.bug_status < Bug_Now_Status.CLOSED).order_by(
            Bugs.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)

    posts = pagination1.items
    flash(posts)
    return render_template('index.html', bugs_list=posts,
                           pagination=pagination1)


@main.route('/newbugs', methods=['GET', 'POST'])
@login_required
def newbug():
    #TODO bugview需要美化
    form = StandardBug()

    # print form.validate_on_submit()
    # print form.errors
    # print form.product_name.data

    product_info = ProductInfo.query.filter_by(product_status=True).all()
    # print [post.product_name_turple() for post in product_info]
    form.product_name.choices = [('-1', u'请选择产品')] + [
        post.product_name_turple() for post in product_info]
    form.product_version.choices = [('-1', u'请选择产品')]
    form.software_version.choices = [('-1', u'请选择产品')]

    # 可以使用重写validation函数来改变验证函数，检查产品版本，只要值不为-1即可
    print form.errors
    print form.validate_on_submit()
    # print request.values
    if form.validate_on_submit():
        # if request.method == 'POST':
        print 'POST'
        print form.validate_on_submit()
        print form.errors
        print form.product_name.data
        if len(form.errors) != 0:
            return render_template("standard_bug.html", form=form)

        print 'errror'
        UPLOAD_FOLDER = 'static/Uploads/'
        app_dir = 'app/'
        f = request.files['attachment']
        fname = None
        print 'eeee'
        is_has_attach_files = False
        if f.filename != '':
            print 'DDDDDDDDD'
            # fname = UPLOAD_FOLDER + secure_filename(f.filename)
            # f.save(app_dir + UPLOAD_FOLDER + secure_filename(f.filename))
            is_has_attach_files = True

        bug = Bugs(bug_id=form.bugs_id.data,
                   product_name=form.product_name.data,
                   product_version=form.product_version.data,
                   software_version=form.software_version.data,
                   version_features=form.version_features.data,
                   bug_level=form.bug_level.data,
                   system_view=form.system_view.data,
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

        # bug_owner_id=form.bug_owner_id.data,
        # bug.timestamp = db.Column(db.DateTime, index=True,
        # default=datetime.utcnow)
        attachments = Attachment.query.filter_by(bug_id=bug.bug_id).all()
        for a in attachments:
            a.confirm = True
        # attachments.confirm = True
        map(db.session.add, attachments)
        process = Process(operator=current_user._get_current_object(),
                          author=User.query.filter_by(
                          email=form.bug_owner_id.data).first(),
                          bugs=bug,
                          old_status='1',
                          new_status=form.bug_status.data,
                          opinion='')
        db.session.add(process)
        db.session.commit()

        flash(u'Bugs 提交成功.')

        # flash(request.files['photo'].filename)
        return redirect(url_for('.bug_process', id=bug.bug_id))
    # flash('Bugs 准备提交.')
    # flash(form.photo.data)
    form.bugs_id.data = Bug_Num_Generate.bug_num()
    read_only(form.bugs_id)
    return render_template("standard_bug.html", form=form)


@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    import mimetypes
    import os
    from tempfile import mktemp
    from werkzeug.utils import secure_filename
    UPLOAD_FOLDER = 'static/Uploads/'
    app_dir = 'app/'
    ALLOWED_MIMETYPES = {'image/jpg', 'image/jpeg', 'image/png', 'image/gif',
                         'image/pjpeg', 'image/x-png'}

    if request.method == 'GET':
        return render_template('upload.html', img='')

    print 'CCCCCCCCCC' ,request.method
    print 'bugs_id  ' ,request.form.get('bugs_id')
    print 'file1 ', request.form.get('system_view')
    print 'file ', request.files['attachment']
    # TODO 关联附件和bug，并显示在页面上
    if request.method == 'POST':
        uploadedFile = request.files['attachment']
        # bug_id = request.args.get('bugs_id')

        # text file treat as binary file.
        # if user wanna post a text file, they would use pastebin / gist.
        if not uploadedFile:
            return abort(400)

        pasteFile = Attachment.create_by_uploadFile(request.form.get('bugs_id'), uploadedFile)
        db.session.add(pasteFile)
        db.session.commit()
        print [pasteFile.url_s , pasteFile.symlink]
        # TODO 返回json优化
        return jsonify({
                "url":pasteFile.url_s ,
                "symlink":pasteFile.symlink,
                "filename":pasteFile.filename})


@main.route('/s/<symlink>')
@login_required
def s(symlink):
    pasteFile = Attachment.get_by_symlink(symlink)

    if not pasteFile:
        return abort(404)

    return redirect(pasteFile.url_p)

@main.route('/p/<filehash>')
@login_required
def p(filehash):
    pasteFile = Attachment.get_by_filehash(filehash)

    if not pasteFile:
        return abort(404)

    return url_for('static', filename='Uploads/' + pasteFile.filehash)

@main.route('/uploads/<filehash>')
@login_required
def uploaded_file(filehash):
    pasteFile = Attachment.get_by_filehash(filehash)

    if not pasteFile:
        return abort(404)
    # current_app.config['UPLOAD_FOLDER'] 在app中显示的是带有app前缀的路径
    import os
    print os.path.join(current_app.config['UPLOAD_FOLDER'], pasteFile.filehash)
    print current_app.config['UPLOAD_FOLDER']
    # return send_from_directory(current_app.config["UPLOAD_FOLDER"], pasteFile.filehash)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], pasteFile.filehash)

@main.route('/bug_process/<string:id>', methods=['GET', 'POST'])
@login_required
def bug_process(id):
    print id
    bugs = Bugs.query.filter_by(bug_id=id).first_or_404()
    attachments = None
    if bugs.bug_attachments:
        attachments = Attachment.query.filter_by(bug_id=id).all()
    # if bugs is None and bugs.status_equal(Bug_Now_Status.CREATED):
    #    return render_template('404.html'), 404

    form = BugsProcess()
    testleadedit = TestLeadEdit()
    developedit = DevelopEdit()
    # developedit.resolve_version.choices  =
    # [('B001','B001'),('B002','B002'),('B003','B003'),('B004','B004')]
    testleadedit2 = TestLeadEdit2()
    bugclose = BugClose()

    if request.method == 'POST' and form.validate():
        print request
        print developedit.validate_on_submit()
        print testleadedit.validate_on_submit()
        print testleadedit2.validate_on_submit()
        print bugclose.validate_on_submit()
        print developedit.errors
        print developedit.dversion_features.data

    if bugs.bug_status == Bug_Now_Status.TESTLEADER_AUDIT \
            and current_user == bugs.bug_owner:
        print 'testleaderedit test'
        if testleadedit.validate_on_submit():
            print 'testleaderedit'
            print testleadedit.bug_status.data
            print developedit.bug_status.data
            bugs.bug_owner_id = User.query.filter_by(
                email=testleadedit.bug_owner_id.data).first().id

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
            '''
            process.author = current_user._get_current_object()
            process.bugs = bugs
            process.status = testleadedit.bug_status.data
            process.opinion = testleadedit.process_opinion'''

            # flash(process_list.timestamp)
            flash('The TestLeader has been updated.')

            return redirect(url_for('.bug_process', id=bugs.bug_id))

    if developedit.validate_on_submit() and current_user == bugs.bug_owner \
            and bugs.bug_status == Bug_Now_Status.DEVELOPMENT:
        print 'developedit'
        print testleadedit.bug_owner_id.data
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
        print 'CCCCC: :', developedit.dresolve_version.data
        db.session.add(bugs)
        db.session.commit()
        flash('The Developer has been updated.')

        return redirect(url_for('.bug_process', id=bugs.bug_id))

    if testleadedit2.validate_on_submit() and current_user == bugs.bug_owner \
            and bugs.bug_status == Bug_Now_Status.TESTLEADER_REGESSION:
        print 'testleadedit2'
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
        flash('The TestLeader2 has been updated.')

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
        flash('The Tester has been updated.')
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

    # form.id.data = bugs.id
    form.product_name.data = bugs.product_name
    form.product_version.data = bugs.product_version
    form.software_version.data = bugs.software_version
    form.version_features.data = bugs.version_features
    form.bug_level.data = bugs.bug_level
    form.system_view.data = bugs.system_view
    form.bug_show_times.data = bugs.bug_show_times
    form.bug_descrit.data = bugs.bug_descrit
    form.bug_title.data = bugs.bug_title

    read_only(form.bug_title)
    read_only(form.product_name)
    read_only(form.product_version)
    read_only(form.software_version)
    read_only(form.version_features)
    read_only(form.bug_level)
    read_only(form.system_view)
    read_only(form.bug_show_times)
    read_only(form.bug_descrit)

    # flash(process_list.first().opinion)
    if bugs.bug_photos is None:
        print 'dddd'
        print 'photo :', bugs.bug_photos
    if bugs.bug_photos is not None:
        print 'ssss'
        flash(bugs.bug_photos)

    return render_template('bugs_process.html',
                           form=form, bugs=bugs, attachments=attachments,
                           testleadedit=testleadedit, developedit=developedit,
                           testleadedit2=testleadedit2, bugclose=bugclose,
                           testmanager_log=testmanager_log,
                           process_log=process_log,
                           developedit_log=developedit_log,
                           bugtest_log=bugtest_log,
                           retest_log=retest_log)


@main.route('/bug_edit/<string:id>', methods=['GET', 'POST'])
@login_required
def bug_edit(id):
    print id
    # bugs = Bugs.query.get_or_404(id)
    # TODO 此处的文件上传未实现
    bugs = Bugs.query.filter_by(bug_id=id).first_or_404()
    attachments = None
    if bugs.bug_attachments:
        attachments = Attachment.query.filter_by(bug_id=id).all()
    # print bugs.now_status.id
    if current_user != bugs.author and \
            bugs.status_equal(Bug_Now_Status.CREATED) and \
            not current_user.can(Permission.ADMINISTER):
        return render_template('404.html'), 404

    process_log = bugs.process.order_by(Process.timestamp.asc())

    form = StandardBug()


    print form.errors
    print form.validate_on_submit()
    if form.validate_on_submit():
        # if request.method == 'POST':
        UPLOAD_FOLDER = 'static/Uploads/'
        app_dir = 'app/'
        f = request.files['attachment']
        fname = None
        print 'ddd'
        if f.filename != '':
            pass
            #fname = UPLOAD_FOLDER + secure_filename(f.filename)
            #f.save(app_dir + UPLOAD_FOLDER + secure_filename(f.filename))
        bugs.product_name = form.product_name.data
        bugs.product_version = form.product_version.data
        bugs.software_version = form.software_version.data
        bugs.version_features = form.version_features.data
        bugs.bug_level = form.bug_level.data
        bugs.system_view = form.system_view.data
        bugs.bug_show_times = form.bug_show_times.data
        bugs.bug_title = form.bug_title.data
        bugs.bug_descrit = form.bug_descrit.data
        bugs.bug_owner = User.query.filter_by(
                            email=form.bug_owner_id.data).first()
        bugs.author = current_user._get_current_object()
        bugs.bug_status = form.bug_status.data
        bugs.bug_photos = fname
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
        flash(bugs.now_status.bug_status_descrit)
        flash('Bugs 提交成功.')
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

    # form.id.data = bugs.id
    form.product_name.data = bugs.product_name
    form.product_version.data = bugs.product_version
    form.software_version.data = bugs.software_version
    form.version_features.data = bugs.version_features
    form.bug_level.data = bugs.bug_level
    form.system_view.data = bugs.system_view
    form.bug_show_times.data = bugs.bug_show_times
    form.bug_descrit.data = bugs.bug_descrit
    form.bug_title.data = bugs.bug_title
    form.bug_owner_id.data = bugs.bug_owner.email
    # form.photo.data = bugs.bug_photos
    # flash(process_list.first().opinion)
    return render_template('bug_edit.html', form=form, attachments=attachments,
                           bugs=bugs, process_log=process_log)


@main.route('/charts', methods=['GET'])
@login_required
def charts():
    return render_template('reports/charts.html')


@main.route('/chartsdata', methods=['GET'])
@login_required
def chartsdata():
    return '''{
            "name":"销量",
            "type":"line",
            "data":[5, 20, 40, 10, 10, 20, 15, 18, 19, 25, 30]
            }'''


@main.route('/dailycharts', methods=['GET'])
@login_required
def dailycharts():
    return render_template('reports/dailycharts.html')


@main.route('/dailydatas', methods=['GET'])
@login_required
def dailydatas():
    # daily_bugs2 = Bugs.query.with_entities(db.func.strftime(
    #        '%Y.%m.%d',Bugs.timestamp).label('date'),
    # db.func.count(Bugs.id).label('total')).group_by(db.func.strftime(
    #       '%Y.%m.%d',Bugs.timestamp).label('date')).all()

    daily_bugs = db.session.query(
                    db.func.strftime('%Y.%m.%d', Bugs.timestamp).label('date'),
                    db.func.count(Bugs.id).label('total')).group_by(
                    db.func.strftime('%Y.%m.%d', Bugs.timestamp)).all()
    # ss = db.session.execute("select strftime('%Y.%m.%d',timestamp)
    # as date,count(id) as total from bugs GROUP BY
    # strftime('%Y.%m.%d',timestamp)")

    return jsonify({
        'name': "Bugs数",
        'type': "bar",
        'data': [s.total for s in daily_bugs],
        'date': [s.date for s in daily_bugs]
        })


@main.route('/productcharts', methods=['GET'])
@login_required
def productcharts():
    # product = ProductInfo.query.all()
    product = ProductInfo.query.filter_by(product_status=True).all()

    return render_template('reports/productcharts.html', product=product)


@main.route('/productdatas', methods=['GET'])
@login_required
def productdatas():
    prd = request.args.get('product')
    # print prd
    daily_bugs = Bugs.query.with_entities(
        db.func.strftime('%Y.%m.%d', Bugs.timestamp).label('date'),
        db.func.count(Bugs.id).label('total')).filter(
        Bugs.product_name == prd).group_by(
        db.func.strftime('%Y.%m.%d', Bugs.timestamp).label('date')).all()

    return jsonify({
        'name': "Bugs2",
        'type': "bar",
        'data': [s.total for s in daily_bugs],
        'date': [s.date for s in daily_bugs]
        })


@main.route('/seriousdatas', methods=['GET'])
@login_required
def seriousdatas():
    prd = request.args.get('product')
    daily_bugs = Bugs.query.with_entities(
                    Bugs.bug_level.label('level'),
                    db.func.count(Bugs.id).label('total')).filter(
                    Bugs.product_name == prd).group_by(
                    Bugs.bug_level.label('level')).all()

    return jsonify({
        'name': "Bugs",
        'type': "bar",
        'data': [s.total for s in daily_bugs],
        'level': [s.level for s in daily_bugs]
        })


@main.route('/seriousdataspie', methods=['GET'])
@login_required
def seriousdataspie():
    prd = request.args.get('product')
    daily_bugs = Bugs.query.with_entities(
                    Bugs.bug_level.label('level'),
                    db.func.count(Bugs.id).label('total')).filter(
                    Bugs.product_name == prd).group_by(
                    Bugs.bug_level.label('level')).all()

    data = [{"value": s.total, "name": s.level} for s in daily_bugs]

    return jsonify({
        'name': "Bugs",
        'type': "bar",
        'data': data,
        'level': [s.level for s in daily_bugs]
        })


@main.route('/statusdatas', methods=['GET'])
@login_required
def statusdatas():
    prd = request.args.get('product')

    # dd = db.session.query(db.func.count(Bugs.id).label('total'),
    # BugStatus.bug_status_descrit.label('status'))
    # ss = dd.join(BugStatus, BugStatus.bug_status==Bugs.bug_status).filter(
    # Bugs.product_name==prd).group_by(Bugs.bug_status).all()
    daily_bugs = db.session.query(
                db.func.count(Bugs.id).label('total'),
                BugStatus.bug_status_descrit.label('status')).filter(
                Bugs.product_name == prd).filter(
                Bugs.bug_status == BugStatus.bug_status).group_by(
                Bugs.bug_status).all()
    # print '44'*20
    # print str(daily_bugs)
    # print '44'*20

    # 直接使用sql语句查询的结果访问属性会失败，返回500的错误
    # daily_bugs = db.session.execute("SELECT bugstatus.bug_status_descrit as
    # bugs_bug_status, count(bugs.id) as total FROM bugs, bugstatus on
    # bugs.bug_status=bugstatus.bug_status WHERE bugs.product_name ='IPC'
    # GROUP BY bugstatus.bug_status")

    return jsonify({
        'name': "Bugs",
        'type': "bar",
        'data': [s.total for s in daily_bugs],
        'status': [s.status for s in daily_bugs]
        })


@main.route('/authordatas', methods=['GET'])
@login_required
def authordatas():
    prd = request.args.get('product')

    daily_bugs = db.session.query(db.func.count(Bugs.id).label('total'),
                                  User.username.label('status')).filter(
                                  Bugs.product_name == prd).filter(
                                  Bugs.author_id == User.id).group_by(
                                  Bugs.author_id).all()

    return jsonify({
        'name': "Bugs",
        'type': "bar",
        'data': [s.total for s in daily_bugs],
        'status': [s.status for s in daily_bugs]
        })


@main.route('/test')
@login_required
def test2():
    print 'test2'
    print request.args.get('search')
    return render_template('autocomplate.html')


@main.route('/autocomplete', methods=['GET'])
@login_required
def autocomplete():
    search = request.args.get('query', 0, type=str)
    print search.isalnum()
    if not search.isalnum():
        return 'Not Found', 200
    user = User.query.filter(User.email.like(search + '%')).all()
    return jsonify({"suggestions":[u.email for u in user]})
