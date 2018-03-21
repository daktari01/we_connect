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
