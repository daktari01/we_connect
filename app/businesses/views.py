import os
from flask import Flask, request, jsonify

# Local imports
from . import busy
from app.models import User, Business, Review
from app.auth.views import token_required

# Create instances of 'model' classes
user = User()
business = Business()
review = Review()

business_i = Business()
reviews_i = Review()

@busy.route('/businesses', methods=['POST'])
@token_required
def fn_create_businesses(current_user):
    """Create business"""
    data = request.get_json()
    business_id = len(business_i.businesses) + 1
    if data['name'] in business_i.businesses:
        return jsonify({"message": "Business name already exists." +  
                " Create another one"})
    new_business = {"business_id":business_id, 
        "user_id":current_user['user_id'],
        "name":data['name'], "location":data['location'], 
        "web_address":data['web_address'],
        "category":data['category']}
    business_i.businesses[data["name"]] = new_business
    return jsonify({"message" : "Business created successfully"}), 201
    
    
@busy.route('/businesses', methods=['GET'])
def fn_get_businesses():
    """Get all businesses"""
    return jsonify(business_i.businesses), 200

@busy.route('/businesses/<int:business_id>', methods=[
    'GET', 'PUT', 'DELETE'])
@token_required
def fn_business(current_user, business_id):
    """Find a single business by ID"""
    single_business = {}
    
    for business in business_i.businesses.values():
        if business['business_id'] == business_id:
            single_business = business

    # Get one business
    if request.method == 'GET':
        if single_business:
            return jsonify(single_business)
        return jsonify({"message" : "Business not found"})
    # Update business details
    if request.method == 'PUT':
        data = request.get_json()
        single_business['name'] = data['name']
        single_business['location'] = data['location']
        single_business['web_address'] = data['web_address']
        single_business['category'] = data['category']
        return jsonify(single_business), 200
    
    # Delete a business
    if request.method == 'DELETE':
        business_i.businesses.pop(single_business['name'])
        return jsonify({"message" : "Business deleted successfully"}), 200

@busy.route('/businesses/<int:business_id>/reviews', 
                methods=['GET', 'POST'])
@token_required
def fn_reviews(current_user ,business_id):
    """Post or view reviews for a business"""
    single_business = {}
    
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
        new_review = {"review_id":review_id, "user_id":current_user['user_id'], 
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