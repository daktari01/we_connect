# api/__init__.py

import uuid
from flask import Flask, request, jsonify, abort, make_response

# Local imports
from config import app_config
from .auth.views import token_required

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
            current_user = "1"
            data = request.get_json()
            new_business_id = 1
            business_id = len(businesses) + 1
            new_business = {"business_id":business_id, 
                "user_id":current_user,
                "name":data['name'], "location":data['location'], 
                "web_address":data['web_address'],
                "category":data['category']}
            businesses["business_id"] = new_business
            return jsonify({"message" : "Business created successfully"}), 201

        if request.method == 'GET':
            return jsonify(businesses), 200
        return jsonify({'message' : 'Invalid input'})

    @app.route('/api/v1/business/<business_id>', methods=[
        'GET', 'PUT', 'DELETE'])
    def fn_business(business_id):
        data = request.get_json()
        single_business = businesses[data['business_id']['name']]
        current_user = "1"

        if not single_business:
            return jsonify({"message" : "Business not found"}), 404

        # Find a single business by business_id
        if request.method == 'GET':
            return jsonify(single_business)
        
        # Update business details
        if request.method == 'PUT':
            single_business['user_id'] = current_user
            single_business['name'] = data['name']
            single_business['location'] = data['location']
            single_business['web_address'] = data['web_address']
            single_business['category'] = data['category']
            return jsonify(single_business), 200
        
        # Delete a business
        if request.method == 'DELETE':
            businesses.pop(single_business['business_id'])
            return jsonify({"message" : "Business deleted successfully"}), 200
            
    return app

