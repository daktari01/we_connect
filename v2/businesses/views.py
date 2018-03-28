import os
import psycopg2
from flask import Flask, request, jsonify

# Local imports
from . import busn
from v2.models import User, Business, Review
from v2.auth.views import token_required
from v2 import db

@busn.route('/businesses', methods=['POST'])
@token_required
def create_business(current_user):
    """Register a business"""
    data = request.get_json()
    web_address_error = {}
    busn_name_error = {}
    businesses = Business.query.all()
    # Get rid of duplicates
    for business in businesses:
        if data['name'] == business.name:
            busn_name_error = {'message':'A business with that name already'+
                                            ' exists. Try another name'}
        if data['web_address'] == business.web_address:
            web_address_error = {'message':'A business with that web address'+
                                        ' already exists. Try another one'}
    if busn_name_error:
        return jsonify(busn_name_error)
    if web_address_error:
        return jsonify(web_address_error)
    new_business = Business(user_id=current_user.id, name=data['name'], 
                    location=data['location'], category = data['category'],
                    web_address = data['web_address'])
    # Save to the database
    try:
        db.session.add(new_business)
        db.session.commit()
        return jsonify({'message': 'Business registered successfully'})
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify(str(error))
    
@busn.route('/businesses', methods=['GET'])
def retrieve_businesses():
    """Get all businesses from the database"""
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=9, type=int)
    businesses = Business.query.paginate(page, limit, error_out=False).items
    output = []
    # Get business data into a list of dictionaries
    for business in businesses:
        business_data = {}
        business_data['user_id'] = business.user_id
        business_data['name'] = business.name
        business_data['location'] = business.location
        business_data['category'] = business.category
        business_data['web_address'] = business.web_address
        output.append(business_data)
    return jsonify({'businesses' : output})

@busn.route('/businesses/<business_id>', methods=['GET'])
def retrieve_one_business(business_id):
    """Retrieve a single business by id"""
    business = Business.query.filter_by(id=business_id).first()
    if not business:
        return jsonify({'message':'Business not found'})
    business_data = {}
    business_data['user_id'] = business.user_id
    business_data['name'] = business.name
    business_data['location'] = business.location
    business_data['category'] = business.category
    business_data['web_address'] = business.web_address
    return jsonify(business_data)

@busn.route('/businesses/<business_id>', methods=['PUT'])
@token_required
def edit_one_business(current_user, business_id):
    """Edit business details"""
    business = Business.query.filter_by(id=business_id).first()
    data = request.get_json()
    if not business:
        return jsonify({'message':'Business not found'})
    if business.user_id != current_user.id:
        return jsonify({'message': 'User can only edit own businesses'})
    business.name = data['name']
    business.location = data['location']
    business.category = data['category']
    business.web_address = data['web_address']
    # Save to the database
    try:
        db.session.commit()
        return jsonify({'message': 'Business edited successfully'})
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify(str(error))

@busn.route('/businesses/<business_id>', methods=['DELETE'])
@token_required
def delete_one_business(current_user, business_id):
    """Delete business details"""
    business = Business.query.filter_by(id=business_id).first()
    if not business:
        return jsonify({'message':'Business not found'})
    if business.user_id != current_user.id:
        return jsonify({'message': 'User can only delete own businesses'})
    db.session.delete(business)
    db.session.commit()
    return jsonify({'message' : 'Business deleted successfully!'})

@busn.route('/businesses/<business_id>/reviews', methods=['POST'])
@token_required
def post_review_for_business(current_user, business_id):
    """Post review for a business"""
    business = Business.query.filter_by(id=business_id).first()
    data = request.get_json()
    if not business:
        return jsonify({'message':'Business not found'})
    new_review = Review(rev_user_id=current_user.id, business_id=business_id,
                        review_title=data['review_title'], 
                        review_text=data['review_text'])
    # Save to the database
    try:
        db.session.add(new_review)
        db.session.commit()
        return jsonify({'message': 'Review posted successfully'})
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify(str(error))

@busn.route('/businesses/<business_id>/reviews', methods=['GET'])
def get_reviews_for_business(business_id):
    """Get all reviews for a business"""
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=5, type=int)
    business = Business.query.filter_by(id=business_id).first()
    if not business:
        return jsonify({'message':'Business not found'})
    reviews = business.reviews.paginate(page, limit, error_out=False).items
    output = []
    # Get review data into a list of dictionaries
    for review in reviews:
        review_data = {}
        review_data['review_title'] = review.review_title
        review_data['review_text'] = review.review_text
        review_data['date_reviewed'] = review.date_reviewed
        output.append(review_data)
    return jsonify({'reviews' : output})
    