#coding=utf-8
from flask import render_template, redirect, request, url_for, flash, \
    current_app, jsonify
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from wtforms_components import read_only
from werkzeug import secure_filename
from .. import db
from . import main
from .forms import StandardBug, BugsProcess, TestLeadEdit, DevelopEdit, \
    TestLeadEdit2, BugClose
from ..email import send_email
from ..models import Bugs, User, Process, BugStatus


@main.route('/')
@login_required
def index():
    #bugs_list = Bugs.query.filter_by(bug_owner=current_user).all()

    page = request.args.get('page', 1, type=int)
    # sts=BugStatus.query.filter_by(id=6).first()

    pagination1 = Bugs.query.filter(
            Bugs.bug_owner==current_user,Bugs.bug_status<6).order_by(
            Bugs.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)

    posts = pagination1.items
    flash(posts)
    return render_template('index.html', bugs_list=posts, pagination=pagination1)

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
    return jsonify(result=a + b)


@main.route('/ss')
@login_required
def ss():
    # http://blog.csdn.net/porschev/article/details/5943579
    # pageIndex=1&pageSize=20
    #page = request.args.get('page', 1, type=int)
    # sts=BugStatus.query.filter_by(id=6).first()
    page = request.args.get('pageIndex', 1, type=int)
    size = request.args.get('pageSize', 1, type=int)
    pagination1 = Bugs.query.filter(
            Bugs.bug_owner==current_user,Bugs.bug_status<6).order_by(
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
    #page = request.args.get('page', 1, type=int)
    page = request.args.get('pageIndex', 1, type=int)
    size = request.args.get('pageSize', 1, type=int)

    pagination = Bugs.query.filter(
            Bugs.bug_owner==current_user,Bugs.bug_status<6).order_by(
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
            Bugs.bug_owner==current_user,Bugs.bug_status<6).order_by(
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

    query = Bugs.query
    q = query.all()
    from datatables import DataTable

    # ('bugs_owner','bug_owner.username'),
    table = DataTable(request.args, Bugs, query, [
        "id",
        ('user_name', 'author.username'),
        "bug_level",
        "bug_owner_id",
        "bug_show_times",
        ('bug_status','now_status.bug_status_descrit'),
        "bug_title",
        "product_name",
        "product_version",
        "software_version",
        "system_view",
        "timestamp"
    ])

    return jsonify(table.json())



@main.route('/task/<string:mytask>')
@login_required
def task(mytask):
    if mytask == 'created':
        page = request.args.get('page', 1, type=int)

        pagination = Bugs.query.filter_by(author=current_user).paginate(
                page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)
        #posts = pagination2.items

    if mytask == 'processed':
        page = request.args.get('page', 1, type=int)

        # 查询的思路是表连接,要去重复值
        pagination = Bugs.query.join(Process, Process.bugs_id==Bugs.id).distinct().filter(
            Process.operator==current_user).paginate(
                page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)

    posts = pagination.items
    flash(str(Bugs.query.join(Process, Process.bugs_id==Bugs.id).filter(
            Process.operator==current_user)))
    return render_template('main.html', bugs_list=posts, pagination=pagination,mytask=mytask)




@main.route('/copy_to_me/')
@login_required
def copy_to_me():
    query = db.session.query(overtimemodel.Statics)
    q = query.all()
    from datatables import DataTable
    table = DataTable(request.args, overtimemodel.Statics, query, [
     ('user_name', 'user.name'),
     'overtime_total',
     'overtime_avail',
     'overtime_holiday',
     'overtime_expense',
     'overtime_shared',
     'invoice_lack_amount'
    ])
    return jsonify(table.json())

@main.route('/newbugs', methods=['GET', 'POST'])
@login_required
def newbug():
    form = StandardBug()
    if request.method == 'POST':
        UPLOAD_FOLDER = 'static/Uploads/'
        app_dir = 'app/'
        f = request.files['photo']
        fname = UPLOAD_FOLDER + secure_filename(f.filename)
        f.save(app_dir + UPLOAD_FOLDER + secure_filename(f.filename))

        bug = Bugs(product_name=form.product_name.data,
        product_version=form.product_version.data,
        software_version=form.software_version.data,
        bug_level=form.bug_level.data,
        system_view=form.system_view.data,
        bug_show_times=form.bug_show_times.data,
        bug_title=form.bug_title.data,
        bug_descrit=form.bug_descrit.data,
        bug_owner=User.query.filter_by(email=form.bug_owner_id.data).first(),
        author=current_user._get_current_object(),
        bug_status=form.bug_status.data,
        bug_photos=fname)

        db.session.add(bug)

        # bug_owner_id=form.bug_owner_id.data,
        # bug.timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
        process = Process(operator=current_user._get_current_object(),
                    author=User.query.filter_by(email=form.bug_owner_id.data).first(),
                            bugs=bug,
                            old_status='1',
                            new_status=form.bug_status.data,
                            opinion='')
        db.session.add(process)
        db.session.commit()


        flash('Bugs 提交成功.')
        flash(request.files['photo'].filename)
        return redirect(url_for('.bug_process', id=bug.id))
    flash('Bugs 提交失败.')
    flash(form.photo.data)
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
    ALLOWED_MIMETYPES = {'image/JPG','image/jpeg', 'image/png', 'image/gif','image/pjpeg','image/x-png',}

    if request.method == 'GET':
        return render_template('upload.html', img='')
    elif request.method == 'POST':
        f = request.files['file']
        print 'ffff   :::::',f.filename
        if f.filename == '':
            flash('No select file')
            return redirect(url_for('main.upload'), 302)
        #fname = mktemp(suffix='_', prefix='u', dir=UPLOAD_FOLDER) + secure_filename(f.filename)
        fname = UPLOAD_FOLDER + secure_filename(f.filename)
        f.save(app_dir + UPLOAD_FOLDER + secure_filename(f.filename))
        if mimetypes.guess_type(fname)[0] in ALLOWED_MIMETYPES:
            flash(app_dir + UPLOAD_FOLDER + secure_filename(f.filename))
            return render_template('upload.html', img=fname)
        else:
            os.remove(app_dir + fname)
            flash(mimetypes.guess_type(fname)[0])
            return redirect(url_for('main.upload'), 302)


@main.route('/bug_process/<int:id>', methods=['GET', 'POST'])
@login_required
def bug_process(id):
    bugs = Bugs.query.get_or_404(id)

    # 处理日志
    process_log = bugs.process.order_by(Process.timestamp.asc())
    testmanager_log = bugs.process.filter_by(old_status='2').order_by(
                        Process.timestamp.desc())
    developedit_log = bugs.process.filter_by(old_status='3').order_by(
                        Process.timestamp.desc())
    bugtest_log = bugs.process.filter_by(old_status='4').order_by(
                        Process.timestamp.desc())
    retest_log = bugs.process.filter_by(old_status='5').order_by(
                        Process.timestamp.desc())
    #post.comments.order_by(Comment.timestamp.asc()) .filter_by(status='3')
    form = BugsProcess()
    testleadedit = TestLeadEdit()
    developedit = DevelopEdit()
    testleadedit2 = TestLeadEdit2()
    bugclose = BugClose()


    if testleadedit.validate_on_submit() and current_user == bugs.bug_owner:
        bugs.bug_owner_id = User.query.filter_by(
            email=testleadedit.bug_owner_id.data).first().id

        process = Process(operator=current_user._get_current_object(),
                        author=User.query.filter_by(
                                email=testleadedit.bug_owner_id.data).first(),
                        bugs=bugs,
                        old_status=bugs.bug_status,
                        new_status=testleadedit.bug_status.data,
                        opinion=testleadedit.process_opinion.data)
        db.session.add(process)


        bugs.bug_status = testleadedit.bug_status.data
        db.session.add(bugs)
        '''
        process.author = current_user._get_current_object()
        process.bugs = bugs
        process.status = testleadedit.bug_status.data
        process.opinion = testleadedit.process_opinion'''

        #flash(process_list.timestamp)
        flash('The TestLeader has been updated.')
        return redirect(url_for('.bug_process', id=bugs.id))

    if developedit.validate_on_submit() and current_user == bugs.bug_owner:
        bugs.bug_owner_id = User.query.filter_by(
            email=developedit.bug_owner_id.data).first().id
        process = Process(operator=current_user._get_current_object(),
                        author=User.query.filter_by(
                                email=testleadedit.bug_owner_id.data).first(),
                        bugs=bugs,
                        old_status=bugs.bug_status,
                        new_status=developedit.bug_status.data,
                        opinion=developedit.process_opinion.data)
        db.session.add(process)


        bugs.bug_status = developedit.bug_status.data
        db.session.add(bugs)
        flash('The Developer has been updated.')

        user = User.query.filter_by(email=testleadedit.bug_owner_id.data).first()

        flash(testleadedit.bug_owner_id.data)

        token = user.generate_confirmation_token()

        send_email(user.email, 'Please Process Bugs',
                       'main/email/bug_process', user=user, id=bugs.id, token=token)

        #send_email(user.email, 'Confirm Your Account',
        #                'auth/email/confirm', user=user, token=token)

        flash('A Email send to author.' + user.email)

        return redirect(url_for('.bug_process', id=bugs.id))

    if testleadedit2.validate_on_submit() and current_user == bugs.bug_owner:
        bugs.bug_owner_id = User.query.filter_by(
            email=testleadedit2.bug_owner_id.data).first().id

        process = Process(operator=current_user._get_current_object(),
                        author=User.query.filter_by(
                                email=testleadedit.bug_owner_id.data).first(),
                        bugs=bugs,
                        old_status=bugs.bug_status,
                        new_status=testleadedit2.bug_status.data,
                        opinion=testleadedit2.process_opinion.data)
        db.session.add(process)

        bugs.bug_status = testleadedit2.bug_status.data
        db.session.add(bugs)
        flash('The TestLeader2 has been updated.')
        return redirect(url_for('.bug_process', id=bugs.id))

    if bugclose.validate_on_submit() and current_user == bugs.bug_owner:
        #bugs.bug_owner_id = User.query.filter_by(
        #    email=bugclose.bug_owner_id.data).first().id
        process = Process(operator=current_user._get_current_object(),
                        author=None,
                        bugs=bugs,
                        old_status=bugs.bug_status,
                        new_status=bugclose.bug_status.data,
                        opinion=bugclose.process_opinion.data)
        db.session.add(process)

        bugs.bug_status = bugclose.bug_status.data
        db.session.add(bugs)
        flash('The Tester has been updated.')
        return redirect(url_for('.bug_process', id=bugs.id))


    #form.id.data = bugs.id
    form.product_name.data = bugs.product_name
    form.product_version.data = bugs.product_version
    form.software_version.data = bugs.software_version
    form.bug_level.data = bugs.bug_level
    form.system_view.data = bugs.system_view
    form.bug_show_times.data = bugs.bug_show_times
    form.bug_descrit.data = bugs.bug_descrit
    form.bug_title.data = bugs.bug_title

    read_only(form.bug_title)
    read_only(form.product_name)
    read_only(form.product_version)
    read_only(form.software_version)
    read_only(form.bug_level)
    read_only(form.system_view)
    read_only(form.bug_show_times)
    read_only(form.bug_descrit)

    #flash(process_list.first().opinion)
    return render_template('bugs.html', form=form, bugs=bugs,
        testleadedit=testleadedit, developedit=developedit,
        testleadedit2=testleadedit2, bugclose=bugclose,
        testmanager_log=testmanager_log,process_log=process_log,
        developedit_log=developedit_log,bugtest_log=bugtest_log,retest_log=retest_log)


@main.route('/bug_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def bug_edit(id):
    bugs = Bugs.query.get_or_404(id)
    process_log = bugs.process.order_by(Process.timestamp.asc())

    form = StandardBug()

    if form.validate_on_submit():
        bugs.product_name = form.product_name.data
        bugs.product_version = form.product_version.data
        bugs.software_version = form.software_version.data
        bugs.bug_level = form.bug_level.data
        bugs.system_view = form.system_view.data
        bugs.bug_show_times = form.bug_show_times.data
        bugs.bug_title = form.bug_title.data
        bugs.bug_descrit = form.bug_descrit.data
        bugs.bug_owner = User.query.filter_by(email=form.bug_owner_id.data).first()
        bugs.author = current_user._get_current_object()
        bugs.bug_status = form.bug_status.data

        db.session.add(bugs)

        # bug_owner_id=form.bug_owner_id.data,
        # bug.timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
        process = Process(operator=current_user._get_current_object(),
                    author=User.query.filter_by(email=form.bug_owner_id.data).first(),
                            bugs=bugs,
                            old_status='1',
                            new_status=form.bug_status.data,
                            opinion='')
        db.session.add(process)
        db.session.commit()
        flash(bugs.now_status.bug_status_descrit)
        flash('Bugs 提交成功.')
        return redirect(url_for('.bug_process', id=bugs.id))

    #form.id.data = bugs.id
    form.product_name.data = bugs.product_name
    form.product_version.data = bugs.product_version
    form.software_version.data = bugs.software_version
    form.bug_level.data = bugs.bug_level
    form.system_view.data = bugs.system_view
    form.bug_show_times.data = bugs.bug_show_times
    form.bug_descrit.data = bugs.bug_descrit
    form.bug_title.data = bugs.bug_title
    form.bug_owner_id.data = bugs.bug_owner.email
    #flash(process_list.first().opinion)
    return render_template('bug_edit.html', form=form, bugs=bugs,process_log=process_log)
