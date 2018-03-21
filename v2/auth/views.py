import os
import jwt
import datetime
import psycopg2

from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps 

# Local imports
from . import auth
from v2.models import User, Business, Review
from v2 import db

def token_required(fn):
    """Decorator to require authentication token"""
    @wraps(fn)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing'}), 401
        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'))
            current_user = User.query.filter_by(username=data[
                                                'username']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return fn(current_user, *args, **kwargs)
    return decorated

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
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'})
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify(str(error))
    

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

@auth.route('/login', methods=['POST'])
def login():
    """Method to log in authenticated user"""
    data = request.get_json()
    # Check if required login information is missing
    if not data['username'] or not data['password']:
        return make_response("WeConnect was unable to authenticate", 401, 
                {'WWW-Authenticate' : 'Basic realm="Login required'})
    user = User.query.filter_by(username=data['username']).first()

    # Check if user is not in system
    if not user:
        return make_response("WeConnect was unable to authenticate", 401, 
                {'WWW-Authenticate' : 'Basic realm="User not found. Register.'})
    # Check if password given matches password in WeConnect
    if check_password_hash(user.first_password, data['password']):
        token = jwt.encode({'username' : user.username, 
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(
                minutes=30)}, os.getenv('SECRET_KEY'))
        return jsonify({'token' : token.decode('UTF-8')}), 200
    # Check if authentication fails
    return make_response("WeConnect was unable to authenticate", 401, 
                {'WWW-Authenticate' : 'Basic realm="Login required'})
                
@auth.route('/reset-password', methods=['POST'])
@token_required
def reset_password(current_user):
    """Reset user password"""
    data = request.get_json()
    user = User.query.filter_by(username=current_user['username']).first()
    old_password = data['old_password']
    new_password = data['new_password']
    confirm_new_password = data['confirm_new_password']
    
    if new_password != confirm_new_password:
        return jsonify({'message': 'Your new password must match the confirm' +
            ' password before it can be reset.'})
    if check_password_hash(current_user['password'], old_password):
        user.users[current_user["username"]][
                "password"] = generate_password_hash(data[
                                'new_password'])
        return jsonify({"message" : "Password reset successful"})
    else:
        return jsonify({'message': 'Your old password must match the current' +
            ' password before it can be reset.'})