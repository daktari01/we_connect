import os
import re
import jwt
import datetime
import psycopg2

from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Local imports
from . import auth
from app.v2.models import User
from app import db

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

def confirm_email(fn):
    """Decorator to require confirmation of email"""
    @wraps(fn)
    def decorated(*args, **kwargs):
        pass

def validate_names(name):
    if re.match(r'^[a-zA-Z]{2,50}$', name):
        return True
    return False
def validate_username(username):
    if re.match(r'^[a-zA-Z0-9]{5,20}$', username):
        return True
    return False
def validate_email(email):
    if re.match(r'^[a-zA-Z0-9_\-\.]{3,}@.*\.[a-z]{2,4}$', email):
        return True
    return False
def validate_password(password):
    if re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])'+
                    '[A-Za-z\d$@$!%*#?&]{8,}$', password):
        return True
    return False

@auth.route('/confirm_email/<token>')
def confirm_email(token):
    pass

@auth.route('/register', methods=['POST'])
def register():
    """Register new user to the system"""
    data = request.get_json()
    users = User.query.all()
    email_error = {}
    username_error = {}
    validation_error = []
    # Validate user input
    if not validate_names(data['first_name']):
        error = {'First name error':
            'First name must contain only alphabets between 2 to 50 characters'}
        validation_error.append(error)
    if not validate_names(data['last_name']):
        error = {'Last name error':
            'Last name must contain only alphabets between 2 to 50 characters'}
        validation_error.append(error)
    if not validate_username(data['username']):
        error = {'Username error':
            'Username must contain only alphanumeric between 5 '+
                                                        'to 20 characters'}
        validation_error.append(error)
    if not validate_email(data['email']):
        error = {'Email error': 'Email is not valid'}
        validation_error.append(error)
    if not validate_password(data['first_password']):
        error = {'Password error': 'Passwords must be at least 8 characters, '+
                'contain at least an alphabet, a digit and a special character'}
        validation_error.append(error)
    if validation_error:
        return jsonify({'Validation erro': validation_error})
    first_password = generate_password_hash(data['first_password'])
    if not check_password_hash(first_password, data['confirm_password']):
        return({'message': 'Your passwords do not match! Try again'})
    confirm_password = generate_password_hash(data['confirm_password'])
    # Get rid of duplicate username and email
    for user in users:
        if data['username'] == user.username:
            username_error = {'message': 'Username already exists.'+
                                        ' Try another one.'}
        if data['email'] == user.email:
            email_error = {'message': 'Email already exists.'+
                                        ' Try another one.'}
    if username_error:
        return jsonify(username_error)
    if email_error:
        return jsonify(email_error)
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
@token_required
def get_users(current_user):
    """Retrieve all users from the database"""
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    search_query = request.args.get('q', default=None, type=str)
    if search_query:
        users = User.query.filter(User.username.ilike('%'+
            search_query+'%')).paginate(page, limit, error_out=False).items
    users = User.query.paginate(page, limit, error_out=False).items
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
    password_error = []
    data = request.get_json()
    user = User.query.filter_by(username=current_user.username).first()
    if not user:
        return jsonify({'message':'User not found.'})
    old_password = data['old_password']
    new_password = data['new_password']
    confirm_new_password = data['confirm_new_password']
    # Validate new password
    if not validate_password(new_password):
        error = {'Password error': 'Passwords must be at least 8 characters, '+
                'contain at least an alphabet, a digit and a special character'}
        password_error.append(error)
    if password_error:
        return jsonify({'Validation error': password_error})
    if new_password != confirm_new_password:
        return jsonify({'message': 'Your new password must match the confirm' +
            ' password before it can be reset.'})
    if check_password_hash(current_user.first_password, old_password):
        user.first_password = generate_password_hash(data[
                                'new_password'])
        user.confirm_password = generate_password_hash(data[
                                'confirm_new_password'])
        return jsonify({"message" : "Password reset successful"})
    else:
        return jsonify({'message': 'Your old password must match the current' +
            ' password before it can be reset.'})
            
@auth.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    return jsonify({'message':'Log out successful'})