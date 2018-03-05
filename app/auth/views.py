from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

from . import auth
# from app import users

users = {}

@auth.route('/register', methods=['POST'])
def register_user():
    """Add a new user to the system"""
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    r_user_id = str(uuid.uuid4())
    new_user = {"user_id":r_user_id, "username":data['username'], 
                "password":hashed_password}
    users[r_user_id] = new_user
    return jsonify({"message" : "User created"}), 201

@auth.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(users), 200

@auth.route('/login', methods=['POST'])
def login():
    # Code to login
    pass

@auth.route('/reset_password', methods=['POST'])
def reset_password():
    # Code to reset password
    pass