# coding=utf-8
from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission, Bugs, Bug_Now_Status


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)

# 检查用户是否有编辑bug的权限
def bug_edit_check(f):
    @wraps(f)
    def decorated_function(bug_id):
        bugs = Bugs.get_by_bug_id(bug_id)
        if not (current_user == bugs.author and \
                bugs.status_equal(Bug_Now_Status.CREATED)) and \
                not current_user.can(Permission.ADMINISTER):
            abort(403)
        return f(bug_id)
    return decorated_function

# 检查用户是否有编辑bug的权限
def bug_edit_check2(sss):
    def decorator(f):
        @wraps(f)
        def decorated_function(bug_id):
            bugs = Bugs.get_by_bug_id(bug_id)
            if not (current_user == bugs.author and \
                    bugs.status_equal(Bug_Now_Status.CREATED)) and \
                    not current_user.can(Permission.ADMINISTER):
                abort(403)
            return f(bug_id)
        return decorated_function
    return decorator