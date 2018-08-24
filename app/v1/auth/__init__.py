from flask import Blueprint

auth_v1 = Blueprint('auth_v1', __name__)

from . import views
