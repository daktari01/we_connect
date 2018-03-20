# v2/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate

# local imports
from config import app_config

db = SQLAlchemy()

def create_app_v2(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    migrate = Migrate(app, db)
    db.init_app(app)
              
    return app
