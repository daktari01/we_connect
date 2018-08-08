import os
import re
import jwt
import datetime
import psycopg2

from flask import Flask, request, jsonify, make_response, url_for, redirect
from flask_mail import Message, Mail
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from itsdangerous import BadTimeSignature
from functools import wraps

# Local imports
from . import auth
from app.v2.models import User
from app import db

# Email configurations
app = Flask(__name__)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

local_url = os.getenv('LOCAL_URL')

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

def email_confirmed(fn):
    """Decorator to require confirmation of email"""
    @wraps(fn)
    def decorated(*args, **kwargs):
        user = args[0]
        if not user.email_confirmed:
            return jsonify({"message": "Your account has not"+
                                        " been activated."}), 401
        return fn(*args, **kwargs)
    return decorated

def token_valid(fn):
    """Decorator to require valid token"""
    @wraps(fn)
    def decorated(*args, **kwargs):
        user = args[0]
        if not user.logged_in:
            return jsonify({"message": "You are logged out. "+
                                        "Login to proceed."}), 401
        return fn(*args, **kwargs)
    return decorated

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
        return jsonify({'Validation error': validation_error}), 400
    first_password = generate_password_hash(data['first_password'])
    if not check_password_hash(first_password, data['confirm_password']):
        return({'message': 'Your passwords do not match! Try again'}), 400
    confirm_password = generate_password_hash(data['confirm_password'])
    # Get rid of duplicate username and email
    for user in users:
        if (data['username']).lower() == (user.username).lower():
            username_error = {'message': 'Username already exists.'+
                                        ' Try another one.'}
        if data['email'] == user.email:
            email_error = {'message': 'Email already exists.'+
                                        ' Try another one.'}
    if username_error:
        return jsonify(username_error), 400
    if email_error:
        return jsonify(email_error), 400
    new_user = User(first_name=data['first_name'], last_name=data['last_name'],
        username=data['username'], email=data['email'],
        first_password=first_password, confirm_password=confirm_password,
        email_confirmed=False, logged_in=False)
    # Save to database
    try:
        db.session.add(new_user)
        db.session.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify(str(error)), 400
    # Send activation email to user
    try:
        email = data['email']
        token = serializer.dumps(email, salt="email-confirmation-salt")
        msg = Message('Confirm email', sender='daktari.weconnect@gmail.com',
                                        recipients=[email])
        link = url_for('auth.confirm_email', token=token, _external=True)
        msg.body = "You are almost there.<br/>Click on this <a href={}>link</a> to activate your WeConnect account".format(link)
        mail.send(msg)
        return jsonify({'message': 'User registered successfully. Check your'+
                                    ' email address for an activation'+
                                    ' link to activate your account'}), 200
    except:
        return jsonify({"message": "Sorry, the link was not "+
                                    "sent. Try again"}), 400

@auth.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    """Method to confirm user email"""
    try:
        email = serializer.loads(token, salt="email-confirmation-salt",
                                            max_age=1800)
    except SignatureExpired:
        return "<h3>Sorry, The token is expired!</h3>"
    except BadTimeSignature:
        return "<h3>Sorry, The token is not correct!</h3>"
    # Activate user email
    user = User.query.filter_by(email=email).first()
    if not user:
        return({"message": "User not found"})
    user.email_confirmed = True
    db.session.commit()
    return redirect(local_url + "/login")

@auth.route('/users', methods=['GET'])
@token_required
@email_confirmed
@token_valid
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
    return jsonify({'users' : output}), 200

@auth.route('/login', methods=['POST'])
def login():
    """Method to log in authenticated user"""
    data = request.get_json()
    # Check if required login information is missing
    if not data['username'] or not data['password']:
        return make_response("Both username and password must be provided.", 401,
                {'WWW-Authenticate' : 'Basic realm="Login required'})
    user = User.query.filter_by(username=data['username']).first()

    # Check if user is not in system
    if not user:
        return make_response("User not found.", 401,
                {'WWW-Authenticate' : 'Basic realm="User not found. Register.'})
    # Check if password given matches password in WeConnect
    if check_password_hash(user.first_password, data['password']):
        token = jwt.encode({'username' : user.username,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(
                minutes=1440)}, os.getenv('SECRET_KEY'))
        user.logged_in = True
        db.session.commit()
        return jsonify({'token' : token.decode('UTF-8'), 'user_id':user.id}), 200
    # Check if authentication fails
    return make_response("Your username does not match the password", 401,
                {'WWW-Authenticate' : 'Basic realm="Login required'})
        
@auth.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset user password"""
    data = request.get_json()
    # Send reset password email to user
    try:
        email = data['email']
        token = serializer.dumps(email, salt="password-reset-salt")
        msg = Message('Reset Password', sender='daktari.weconnect@gmail.com', 
                                        recipients=[email])
        link = local_url + "/reset/" + token
        msg.body = "Click on this link to reset your password {}".format(link)
        mail.send(msg)
        return jsonify({'message': 'Check your email address for a link to'+
                                    ' reset your account password.'}), 200
    except:
        return jsonify({"message": "Sorry, the link was not "+
                                    "sent. Try again"}), 400


@auth.route('/reset/<token>', methods=['GET','POST'])
def reset(token):
    """Reset user password"""
    try:
        email = serializer.loads(token, salt="password-reset-salt",
                                            max_age=1800)
    except SignatureExpired:
        return jsonify({"message":"Sorry, The token is expired!"}), 400
    except BadTimeSignature:
        return jsonify({"message":"Sorry, The token is not correct!"}), 400
    password_error = []
    data = request.get_json()
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message':'User not found.'}), 404
    new_password = data['new_password']
    confirm_new_password = data['confirm_new_password']
    # Validate new password
    if not validate_password(new_password):
        error = {'Password error': 'Passwords must be at least 8 characters, '+
                'contain at least an alphabet, a digit and a special character'}
        password_error.append(error)
    if password_error:
        return jsonify({'Validation error': password_error}), 400
    if new_password != confirm_new_password:
        return jsonify({'message': 'Your new password must match the confirm' +
            ' password before it can be reset.'}), 400
    # Reset the user password
    user.first_password = generate_password_hash(new_password)
    user.confirm_password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({'message': 'Your password has been reset '+
                                    'successfully. You can now log in'}), 200
            
@auth.route('/logout', methods=['POST'])
@token_required
@email_confirmed
@token_valid
def logout(current_user):
    current_user.logged_in = False
    db.session.commit()
    return jsonify({'message':'Log out successful'}), 200