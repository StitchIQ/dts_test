from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, \
	current_user
from .. import db
from . import main
from .forms import StandardBug
from ..models import Bugs, User


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/newbugs', methods=['GET', 'POST'])
@login_required
def newbug():
	form = StandardBug()
	if form.validate_on_submit():
		bug = Bugs(product_name=form.product_name.data,
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