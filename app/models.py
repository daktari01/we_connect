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

class Business:
    """Contains data for businesses"""
    def __init__(self):
        """Initialize methods to be used"""
        self.businesses = {}

class Review:
    """Contains data for reviews"""
    def __init__(self):
        """Initialize methods to be used"""
        self.reviews =  {}
        