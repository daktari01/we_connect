from flask import Blueprint

busy_v1 = Blueprint('busy_v1', __name__)

from . import views



