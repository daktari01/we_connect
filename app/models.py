from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os
import jwt
from functools import wraps 

class User:
    """Contains data for users"""
    def __init__(self):
        """Initialize methods to be used"""
        self.users = {}

    def md_register_user(self):
        """Add a new user to the system"""
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'])
        r_user_id = str(uuid.uuid4())
        if data['username'] in self.users:
            return jsonify({"message": "User already exists. Please login"})
        new_user = {"user_id":r_user_id, "username":data['username'], 
                    "password":hashed_password}
        self.users[data['username']] = new_user

    def md_get_all_users(self):
        """View all users in the system"""
        pass

class Business:
    """Contains data for businesses"""
    def __init__(self):
        """Initialize methods to be used"""
        pass

class Review:
    """Contains data for reviews"""
    def __init__(self):
        """Initialize methods to be used"""
        pass
        