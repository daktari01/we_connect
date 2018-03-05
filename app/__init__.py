# api/__init__.py 

from flask import Flask, request, jsonify, abort, make_response

# Local imports
from config import app_config

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    # Register the auth blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')

    # Initialize variables
    # users, businesses, reviews = {}

    @app.route('/businesses/', methods=['POST', 'GET'])
    def businesses():
        pass

    return app