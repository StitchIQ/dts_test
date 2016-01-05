from flask import Blueprint

mang = Blueprint('mang', __name__, static_folder='static')

from . import views