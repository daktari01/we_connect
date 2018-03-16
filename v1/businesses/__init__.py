from flask import Blueprint

busy = Blueprint('busy', __name__)

from . import views



