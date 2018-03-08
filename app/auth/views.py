from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os
import jwt
from functools import wraps 

# Local imports
from . import auth
from app.models import User, Business, Review

# Create instances of 'model' classes
user = User()
business = Business()
review = Review()

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
            current_user = users[data['username']]['username']
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return fn(current_user, *args, **kwargs)
    return decorated

@auth.route('/register', methods=['POST'])
def register_user():
    user.md_register_user()
    return jsonify({"message" : "User created"}), 201

@auth.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    return jsonify(user.users), 200

@auth.route('/login', methods=['POST'])
def login():
    """Authenticate user and allow or deny user access"""
    autho = request.get_json()
    # Check if required login information is missing
    if not autho['username'] or not autho['password']:
        return make_response("WeConnect was unable to authenticate", 401, 
                {'WWW-Authenticate' : 'Basic realm="Login required'})

    # Check if user is not in system
    if autho['username'] not in users:
        return make_response("WeConnect was unable to authenticate", 401, 
                {'WWW-Authenticate' : 'Basic realm="Login required'})

    # Check if password given matches password in WeConnect
    if check_password_hash(users[autho['username']]["password"], 
                autho['password']):
        token = jwt.encode({'user_id' : users[autho['username']]["user_id"]},
        os.getenv('SECRET_KEY'))
        return jsonify({'token' : token.decode('UTF-8')}), 200
    # Check if authentication fails
    return make_response("WeConnect was unable to authenticate", 401, 
                {'WWW-Authenticate' : 'Basic realm="Login required'})


@auth.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset user password"""
    data = request.get_json()
    users[data["username"]]["password"] = generate_password_hash(data['password'])
    return jsonify({"message" : "Password reset successful"})

@auth.route('/logout', methods=['POST'])
def logout():
    """Log user out"""
    # Get the token and make it None
    return jsonify({"message": "You are now logged out"})
    