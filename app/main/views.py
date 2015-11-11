from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, \
	current_user

from . import main
from .forms import StandardBug


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/newbugs', methods=['GET', 'POST'])
@login_required
def newbug():
    form = StandardBug()
    if form.validate_on_submit():
        flash('Bugs password.')
    return render_template("standard_bug.html", form=form)

'''
@main.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)
'''