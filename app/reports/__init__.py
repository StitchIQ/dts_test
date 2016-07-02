# coding=utf-8
from flask import Blueprint
reports = Blueprint('reports', __name__, static_folder='static')
from . import views
from ..models import Bug_Now_Status


