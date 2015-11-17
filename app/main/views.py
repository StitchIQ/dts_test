#coding=utf-8
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, \
	current_user
from wtforms_components import read_only
from .. import db
from . import main
from .forms import StandardBug, BugsProcess
from ..models import Bugs, User


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
		author=current_user._get_current_object())

		db.session.add(bug)
		db.session.commit()
		# bug_owner_id=form.bug_owner_id.data,
		# bug.timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
		flash('Bugs 提交成功.')
		return redirect(url_for('.bug_process', id=33))
	return render_template("standard_bug.html", form=form)


@main.route('/bug_process/<int:id>', methods=['GET', 'POST'])
@login_required
def bug_process(id):
    post = Bugs.query.get_or_404(id)
    form = BugsProcess()
    if form.validate_on_submit() and current_user == post.author:
        post.bug_descrit = form.bug_descrit.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.bug_process', id=post.id))
    #form.id.data = post.id
    form.product_name.data = post.product_name
    form.product_version.data = post.product_version
    form.software_version.data = post.software_version
    form.bug_level.data = post.bug_level
    form.system_view.data = post.system_view
    form.bug_show_times.data = post.bug_show_times
    form.bug_descrit.data = post.bug_descrit
    form.bug_title.data = post.bug_title

    read_only(form.bug_title)
    read_only(form.product_name)
    read_only(form.product_version)
    read_only(form.software_version)
    read_only(form.bug_level)
    read_only(form.system_view)
    read_only(form.bug_show_times)
    read_only(form.bug_descrit)

    return render_template('bugs.html', form=form)
