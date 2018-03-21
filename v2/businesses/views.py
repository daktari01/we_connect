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
    new_business = Business(user_id=current_user['id'], name=data['name'], 
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
    businesses = Business.query.all()
    output = []
    # Get user data into a list of dictionaries
    for business in businesses:
        business_data = {}
        business_data['user_id'] = business_data.user_id
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
    business_data['user_id'] = business_data.user_id
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
    if business.user_id != current_user['id']:
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