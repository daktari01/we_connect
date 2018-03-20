# v2/models.py

from v2.create_app_v2 import db 

class User(db.Model):
    """Class for the users model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    confirm_password = db.Column(db.String(200))
    businesses = db.relationship('Business', backref='user', lazy='dynamic')
    reviews = db.relationship('Review', backref='review', lazy='dynamic')
    
class Business(db.Model):
    """Class for the businesses model"""
    __tablename__ = 'businesses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), index=True, unique=True)
    location = db.Column(db.String(100), index=True)
    category = db.Column(db.String(100), index=True)
    web_address = db.Column(db.String(100), unique=True)
    reviews = db.relationship('Review', backref='review', lazy='dynamic')
    
class Review(db.Model):
    """Class for reviews model"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    review_title = db.Column(db.String(150))
    review_text = db.Column(db.Text)
    date_reviewed = db.Column(db.DateTime, default=db.func.current_timestamp())
