# api/__init__.py

import uuid
import requests
from flask import Flask, request, jsonify, abort, make_response

# Local imports
from config import app_config

businesses = {}
reviews = {}

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    # Register the auth blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')

    @app.route('/api/v1/businesses', methods=['POST', 'GET'])
    def fn_businesses():
        """Create business and get all businesses"""
        
        if request.method == 'POST':
            data = request.get_json()
            r_business_id = str(uuid.uuid4())
            new_business = {"business_id":r_business_id, 
                "name":data['name'], "location":data['location'], 
                "web_address":data['web_address'],
                "category":data['category']}
            businesses[r_business_id] = new_business
            return jsonify({"message" : "Business created successfully"}), 201

        if request.method == 'GET':
            return jsonify(businesses), 200
        return jsonify({'message' : 'Invalid input'})

    @app.route('/api/v1/business/<business_id>', methods=['GET', 'PUT', 'DELETE'])
    def fn_business(business_id):
        # user = 
        # if request.method == 'GET':
        pass


    return app

