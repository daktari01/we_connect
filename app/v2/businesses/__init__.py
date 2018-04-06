from flask import Blueprint

busn = Blueprint('busn', __name__)

from . import views