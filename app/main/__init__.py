# coding=utf-8
from flask import Blueprint
main = Blueprint('main', __name__, static_folder='static')
from . import views, errors
from ..models import Bug_Now_Status

# 把变量注册到main全局
@main.app_context_processor
def inject_bug_now_status():
    return dict(Bug_Now_Status=Bug_Now_Status)
