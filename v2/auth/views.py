import os
import jwt
import datetime

from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps 

# Local imports
from . import auth
from v2.models import User, Business, Review
from v2 import db

@auth.route('/register', methods=['POST'])
def register():
    """Register new user to the system"""
    data = request.get_json()
    first_password = generate_password_hash(data['first_password'])
    if not check_password_hash(first_password, data['confirm_password']):
        return({'message': 'Your passwords do not match! Try again'})
    confirm_password = generate_password_hash(data['confirm_password'])
    new_user = User(first_name=data['first_name'], last_name=data['last_name'],
        username=data['username'], email=data['email'], 
        first_password=first_password, confirm_password=confirm_password)
    # Save to database
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@auth.route('/users', methods=['GET'])
def get_users():
    """Retrieve all users from the database"""
    users = User.query.all()
    output = []
    # Get user data into a list of dictionaries
    for user in users:
        user_data = {}
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        user_data['username'] = user.username
        user_data['email'] = user.email
        output.append(user_data)
    return jsonify({'users' : output})
