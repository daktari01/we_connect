# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

# Local imports
from config import app_config

db = SQLAlchemy()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
    app.config.from_pyfile('config.cfg')
    migrate = Migrate(app, db)
    mail.init_app(app)
    with app.app_context():
        db.init_app(app)

    # Register the auth_v1 blueprint
    from app.v1.auth import auth_v1 as auth_blueprint_v1
    app.register_blueprint(auth_blueprint_v1, url_prefix='/api/v1/auth')

    # Register the busy_v1 blueprint
    from app.v1.businesses import busy_v1 as busy_blueprint_v1
    app.register_blueprint(busy_blueprint_v1, url_prefix='/api/v1')

    # Register the auth_v2 blueprint
    from app.v2.auth import auth as auth_blueprint_v2
    app.register_blueprint(auth_blueprint_v2, url_prefix='/api/v2/auth')

    # Register the busy_v2 blueprint
    from app.v2.businesses import busn as busn_blueprint_v2
    app.register_blueprint(busn_blueprint_v2, url_prefix='/api/v2')

    return app