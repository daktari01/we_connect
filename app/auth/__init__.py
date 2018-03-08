from flask import Blueprint

auth = Blueprint('auth', __name__)

from app.models import User, Business, Review

user = User()
business = Business()
review = Review()

from . import views
