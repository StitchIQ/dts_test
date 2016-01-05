#coding=utf-8
from flask import render_template, redirect, request, url_for, flash, \
    current_app, jsonify
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from .. import db
from . import mang
from ..models import Bugs, User, Process, BugStatus


@mang.route('/')
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
    return render_template('mang/add_product.html', bugs_list=posts, pagination=pagination1)
    #return render_template('mang/add_product.html')



