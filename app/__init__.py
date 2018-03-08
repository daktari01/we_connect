# api/__init__.py

import uuid
from flask import Flask, request, jsonify, abort, make_response

# Local imports

from config import app_config
from .auth.views import token_required
from . import models
from app.models import Business, Review

business_i = Business()
reviews_i = Review()

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
            business_id = len(business_i.businesses) + 1
            if data['name'] in business_i.businesses:
                return jsonify({"message": "Business name already exists." +  
                        " Create another one"})
            new_business = {"business_id":business_id, 
                "user_id":current_user,
                "name":data['name'], "location":data['location'], 
                "web_address":data['web_address'],
                "category":data['category']}
            business_i.businesses[data["name"]] = new_business
            return jsonify({"message" : "Business created successfully"}), 201

        if request.method == 'GET':
            return jsonify(business_i.businesses), 200
        return jsonify({'message' : 'Invalid input'})

    @app.route('/api/v1/business/<int:business_id>', methods=[
        'GET', 'PUT', 'DELETE'])
    def fn_business(business_id):
        """Find a single business by ID"""
        single_business = {}
        current_user = "1"
        
        for business in business_i.businesses.values():
            if business.get('business_id') == business_id:
                single_business = business
            else:
                return jsonify({"message" : "Business not found"}), 404

        # Get one business
        if request.method == 'GET':
            print(single_business)
            return jsonify(single_business)
             
        # Update business details
        if request.method == 'PUT':
            data = request.get_json()
            single_business['user_id'] = current_user
            single_business['name'] = data['name']
            single_business['location'] = data['location']
            single_business['web_address'] = data['web_address']
            single_business['category'] = data['category']
            return jsonify(single_business), 200
        
        # Delete a business
        if request.method == 'DELETE':
            business_i.businesses.pop(single_business['name'])
            return jsonify({"message" : "Business deleted successfully"}), 200

    @app.route('/api/v1/business/<int:business_id>/reviews', 
                    methods=['GET', 'POST'])
    def fn_reviews(business_id):
        """Post or view reviews for a business"""
        single_business = {}
        current_user = "1"
        
        for business in business_i.businesses.values():
            if business['business_id'] == business_id:
                single_business = business
            if not single_business:
                return jsonify({"message" : "Business not found"}), 404
        # Post a review for a business
        if request.method == 'POST':
            data = request.get_json()
            biz_id = single_business['business_id']
            review_id = len(reviews_i.reviews)+1
            new_review = {"review_id":review_id, "user_id":current_user, 
                            "business_id":biz_id, 
                            "review_title":data['review_title'],
                            "review_text":data['review_text']}
            reviews_i.reviews['review_id'] = new_review
            return jsonify({"message": "Review posted successfully"})

        # Get all reviews for a business
        if request.method == 'GET':
            business_review = {}
            for biz_review in reviews_i.reviews.values():
               
                if biz_review['business_id'] == business_id:
                    business_review.update(biz_review)
            return jsonify(business_review) 
              

    return app
