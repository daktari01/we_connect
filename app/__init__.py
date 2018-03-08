# api/__init__.py

import uuid
from flask import Flask, request, jsonify, abort, make_response

# Local imports

from config import app_config
from .auth.views import token_required
from . import models
from app.models import Business, Review



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    # Register the auth blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')

    # Register the busy blueprint
    from .businesses import busy as busy_blueprint
    app.register_blueprint(busy_blueprint, url_prefix='/api/v1/businesses')
              
    return app
