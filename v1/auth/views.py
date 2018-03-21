from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os
import jwt
import datetime
from functools import wraps 

# Local imports
from . import auth
from v1.models import User

# Create instances of 'model' classes
user = User()

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
            current_user = user.users[data['username']]
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return fn(current_user, *args, **kwargs)
    return decorated

@auth.route('/register', methods=['POST'])
def register_user():
    """Add a new user to the system"""
    data = request.get_json()
    r_user_id = str(uuid.uuid4())
    email_error = {}
    password_error = {}
    # Check for duplicate username entry
    if data['username'] in user.users:
        return jsonify({"message": "Username already exists." \
                    " Try another one"})
    # Check for duplicate email entry 
    for one_user in user.users.values():
        if one_user.get('email') == data['email']:
            email_error = {"message": "Email already exists. Try another one"}
    if email_error:
        return jsonify(email_error)
    # Check if password matches confirm password 
    if data['password'] != data['confirm_password']:
        password_error = {"message": "Your passwords do not match. Try again"}
    if password_error:
        return jsonify(password_error)
    hashed_password = generate_password_hash(data['password'])
    # Create user if everything is OK
    new_user = {"user_id":r_user_id, "username":data['username'], 
                "name":data['name'], "email":data['email'],
                "password":hashed_password}
    user.users[data['username']] = new_user
    return jsonify({"message" : "User registered successfully"}), 201

@auth.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    """Get all users"""
    if not current_user:
        return jsonify({'message': 
            'You are not allowed to perform this function'}), 401
    return jsonify(user.users), 200

@auth.route('/login', methods=['POST'])
def login():
    """Authenticate user and allow or deny user access"""
    data = request.get_json()
    # Check if required login information is missing
    if not data['username'] or not data['password']:
        return make_response("WeConnect was unable to authenticate", 401, 
                {'WWW-Authenticate' : 'Basic realm="Login required'})

    # Check if user is not in system
    if data['username'] not in user.users:
        return make_response("WeConnect was unable to authenticate", 401, 
                {'WWW-Authenticate' : 'Basic realm="User not found. Register.'})

    # Check if password given matches password in WeConnect
    if check_password_hash(user.users[data['username']]["password"], 
                data['password']):
        token = jwt.encode({'username' : user.users[data['username']]["username"], 
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(
                minutes=30)}, os.getenv('SECRET_KEY'))
        return jsonify({'token' : token.decode('UTF-8')}), 200
    # Check if authentication fails
    return make_response("WeConnect was unable to authenticate", 401, 
                {'WWW-Authenticate' : 'Basic realm="Login required'})

    # auth = request.authorization

    # if not auth or not auth.username or not auth.password:
    #     return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})
    
    # user = User.query.filter_by(username=auth.username).first()

    # if not user:
    #     return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

    # if check_password_hash(user.password, auth.password):
    #     token = jwt.encode({'public_id' : user.public_id, 
    #         'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 
    #             os.getenv('SECRET_KEY'))    
    
    #     return jsonify({'token' : token.decode('UTF-8')})
    # return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})



@auth.route('/reset-password', methods=['POST'])
@token_required
def reset_password(current_user):
    """Reset user password"""
    data = request.get_json()
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

@auth.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Log user out"""
    # Get the token and make it None
    return jsonify({"message": "You are now logged out"})
    