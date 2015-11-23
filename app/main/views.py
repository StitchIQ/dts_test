#coding=utf-8
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from wtforms_components import read_only
from .. import db
from . import main
from .forms import StandardBug, BugsProcess, TestLeadEdit, DevelopEdit, \
    TestLeadEdit2, BugClose
from ..models import Bugs, User, Process


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/newbugs/', methods=['GET', 'POST'])
@login_required
def newbug():
    form = StandardBug()
    if form.validate_on_submit():
        bug = Bugs(product_name=form.product_name.data,
        product_version=form.product_version.data,
        software_version=form.software_version.data,
        bug_level=form.bug_level.data,
        system_view=form.system_view.data,
        bug_show_times=form.bug_show_times.data,
        bug_title=form.bug_title.data,
        bug_descrit=form.bug_descrit.data,
        bug_owner_id=User.query.filter_by(email=form.bug_owner_id.data).first().id,
        author=current_user._get_current_object(),
        bug_status=form.bug_status.data)

        db.session.add(bug)
        db.session.commit()
        # bug_owner_id=form.bug_owner_id.data,
        # bug.timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
        process = Process(author=current_user._get_current_object(),
                                 bugs=bug,
                                 status='2',
                                 opinion='')
        db.session.add(process)

        flash('Bugs 提交成功.')
        return redirect(url_for('.bug_process', id=bug.id))
    #flash('Bugs 提交失败.')
    return render_template("standard_bug.html", form=form)


@main.route('/bug_process/<int:id>', methods=['GET', 'POST'])
@login_required
def bug_process(id):
    bugs = Bugs.query.get_or_404(id)
    process_log = bugs.process.order_by(Process.timestamp.desc())
    process_list = bugs.process.order_by(Process.timestamp.desc())
    #post.comments.order_by(Comment.timestamp.asc()) .filter_by(status='3')
    form = BugsProcess()
    testleadedit = TestLeadEdit()
    developedit = DevelopEdit()
    testleadedit2 = TestLeadEdit2()
    bugclose = BugClose()


    if testleadedit.validate_on_submit() and current_user == bugs.bug_owner:
        bugs.bug_owner_id = User.query.filter_by(
            email=testleadedit.bug_owner_id.data).first().id
        bugs.bug_status = testleadedit.bug_status.data
        db.session.add(bugs)
        '''
        process.author = current_user._get_current_object()
        process.bugs = bugs
        process.status = testleadedit.bug_status.data
        process.opinion = testleadedit.process_opinion'''
        process = Process(author=current_user._get_current_object(),
                        bugs=bugs,
                        status=testleadedit.bug_status.data,
                        opinion=testleadedit.process_opinion.data)
        db.session.add(process)
        #flash(process_list.timestamp)
        flash('The TestLeader has been updated.')
        return redirect(url_for('.bug_process', id=bugs.id))

    if developedit.validate_on_submit() and current_user == bugs.bug_owner:
        bugs.bug_owner_id = User.query.filter_by(
            email=developedit.bug_owner_id.data).first().id
        bugs.bug_status = developedit.bug_status.data
        db.session.add(bugs)

        process = Process(author=current_user._get_current_object(),
                        bugs=bugs,
                        status=developedit.bug_status.data,
                        opinion=developedit.process_opinion.data)
        db.session.add(process)
        flash('The Developer has been updated.')
        return redirect(url_for('.bug_process', id=bugs.id))

    if testleadedit2.validate_on_submit() and current_user == bugs.bug_owner:
        bugs.bug_owner_id = User.query.filter_by(
            email=testleadedit2.bug_owner_id.data).first().id
        bugs.bug_status = testleadedit2.bug_status.data
        db.session.add(bugs)

        process = Process(author=current_user._get_current_object(),
                        bugs=bugs,
                        status=testleadedit2.bug_status.data,
                        opinion=testleadedit2.process_opinion.data)
        db.session.add(process)

        flash('The TestLeader2 has been updated.')
        return redirect(url_for('.bug_process', id=bugs.id))

    if bugclose.validate_on_submit() and current_user == bugs.bug_owner:
        #bugs.bug_owner_id = User.query.filter_by(
        #    email=bugclose.bug_owner_id.data).first().id
        bugs.bug_status = bugclose.bug_status.data
        db.session.add(bugs)

        process = Process(author=current_user._get_current_object(),
                        bugs=bugs,
                        status=bugclose.bug_status.data,
                        opinion=bugclose.process_opinion.data)
        db.session.add(process)

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
        process_list=process_list,process_log=process_log)
