# v2/models.py

from v2 import db 

class User(db.Model):
    """Class for the users model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    
