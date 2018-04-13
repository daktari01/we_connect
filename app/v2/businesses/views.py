import re
import psycopg2
from flask import request, jsonify

# Local imports
from . import busn
from app.v2.models import Business, Review
from app.v2.auth.views import token_required
from app import db

def validate_business_name(name):
    if re.match(r'^(?=.*[A-Za-z])[a-zA-Z0-9\s]{2,50}$', name):
        return True
    return False
def validate_web_address(address):
    if re.match(r'(https:\/\/www\..*\.[a-z]{2,4}|http:\/\/www\..*\.[a-z]{2,4})',
                                                                    address):
        return True
    return False
def validate_location(location):
    if re.match(r'^(?=.*[A-Za-z])[a-zA-Z0-9\s,]{2,100}$', location):
        return True
    return False
def validate_category(category):
    if re.match(r'^(?=.*[A-Za-z])[a-zA-Z0-9\s,]{2,100}$', category):
        return True
    return False
def validate_review_title(title):
    if re.match(r'^(?=.*[A-Za-z])[a-zA-Z0-9\s]{2,100}$', title):
        return True
    return False
def validate_review_text(text):
    if re.match(r'^(?=.*[A-Za-z])[^!@#\$%\^\*:]{2,200}$', text):
        return True
    return False
@busn.route('/businesses', methods=['POST'])
@token_required
def create_business(current_user):
    """Register a business"""
    data = request.get_json()
    web_address_error = {}
    busn_name_error = {}
    validation_error = []
    businesses = Business.query.all()
    # Validate user input
    if not validate_business_name(data['name']):
        error = {'Business name error': 'Business name can only contain '+
                    'aplhanumeric and spaces with characters between 2-50'}
        validation_error.append(error)
    if not validate_web_address(data['web_address']):
        error = {'Web address error': 'Web address is invalid. Provide only '+
                                'the stem URL. It must contain http or https.'}
        validation_error.append(error)
    if not validate_location(data['location']):
        error = {'Location error': 'Location can only contain alphanumeric,'+
                            ' spaces and commas with characters between 2-100'}
        validation_error.append(error)
    if not validate_category(data['category']):
        error = {'Category error': 'Category can only contain alphabets and'+
                            ' spaces with characters between 2-100'}
        validation_error.append(error)
    if validation_error:
        return jsonify(validation_error)
    # Get rid of duplicates
    for business in businesses:
        if data['name'] == business.name:
            busn_name_error = {'message':'A business with that name already'+
                                            ' exists. Try another name'}
        if data['web_address'] == business.web_address:
            web_address_error = {'message':'A business with that web address'+
                                        ' already exists. Try another one'}
    if busn_name_error:
        return jsonify(busn_name_error)
    if web_address_error:
        return jsonify(web_address_error)
    new_business = Business(user_id=current_user.id, name=data['name'],
                    location=data['location'], category = data['category'],
                    web_address = data['web_address'])
    # Save to the database
    try:
        db.session.add(new_business)
        db.session.commit()
        return jsonify({'message': 'Business registered successfully'})
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify(str(error))

@busn.route('/businesses', methods=['GET'])
def retrieve_businesses():
    """Get all businesses from the database"""
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=9, type=int)
    search_query = request.args.get('q', default=None, type=str)
    search_category = request.args.get('category', default=None, type=str)
    search_location = request.args.get('location', default=None, type=str)
    if search_query:
        businesses = Business.query.filter(Business.name.ilike('%'+
            search_query+'%')).paginate(page, limit, error_out=False).items
    elif search_category:
        businesses = Business.query.filter(Business.category.ilike('%'+
            search_category+'%')).paginate(page, limit, error_out=False).items
    elif search_location:
        businesses = Business.query.filter(Business.location.ilike('%'+
            search_location+'%')).paginate(page, limit, error_out=False).items
    else:
        businesses = Business.query.paginate(
                                    page, limit, error_out=False).items
    output = []
    # Get business data into a list of dictionaries
    for business in businesses:
        business_data = {}
        business_data['user_id'] = business.user_id
        business_data['name'] = business.name
        business_data['location'] = business.location
        business_data['category'] = business.category
        business_data['web_address'] = business.web_address
        output.append(business_data)
    return jsonify({'businesses' : output})

@busn.route('/businesses/<business_id>', methods=['GET'])
def retrieve_one_business(business_id):
    """Retrieve a single business by id"""
    business = Business.query.filter_by(id=business_id).first()
    if not business:
        return jsonify({'message':'Business not found'})
    business_data = {}
    business_data['user_id'] = business.user_id
    business_data['name'] = business.name
    business_data['location'] = business.location
    business_data['category'] = business.category
    business_data['web_address'] = business.web_address
    return jsonify(business_data)

@busn.route('/businesses/<business_id>', methods=['PUT'])
@token_required
def edit_one_business(current_user, business_id):
    """Edit business details"""
    validation_error = []
    business = Business.query.filter_by(id=business_id).first()
    data = request.get_json()
    # Validate user input
    if not validate_business_name(data['name']):
        error = {'Business name error': 'Business name can only contain '+
                    'aplhanumeric and spaces with characters between 2-50'}
        validation_error.append(error)
    if not validate_web_address(data['web_address']):
        error = {'Web address error': 'Web address is invalid. Provide only '+
                                'the stem URL. It must contain http or https.'}
        validation_error.append(error)
    if not validate_location(data['location']):
        error = {'Location error': 'Location can only contain alphanumeric,'+
                            ' spaces and commas with characters between 2-100'}
        validation_error.append(error)
    if not validate_category(data['category']):
        error = {'Category error': 'Category can only contain alphabets and'+
                            ' spaces with characters between 2-100'}
        validation_error.append(error)
    if validation_error:
        return jsonify({'Business validation error' : validation_error})
    if not business:
        return jsonify({'message':'Business not found'})
    if business.user_id != current_user.id:
        return jsonify({'message': 'User can only edit own businesses'})
    business.name = data['name']
    business.location = data['location']
    business.category = data['category']
    business.web_address = data['web_address']
    # Save to the database
    try:
        db.session.commit()
        return jsonify({'message': 'Business edited successfully'})
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify(str(error))

@busn.route('/businesses/<business_id>', methods=['DELETE'])
@token_required
def delete_one_business(current_user, business_id):
    """Delete business details"""
    business = Business.query.filter_by(id=business_id).first()
    if not business:
        return jsonify({'message':'Business not found'})
    if business.user_id != current_user.id:
        return jsonify({'message': 'User can only delete own businesses'})
    db.session.delete(business)
    db.session.commit()
    return jsonify({'message' : 'Business deleted successfully!'})

@busn.route('/businesses/<business_id>/reviews', methods=['POST'])
@token_required
def post_review_for_business(current_user, business_id):
    """Post review for a business"""
    review_error = []
    business = Business.query.filter_by(id=business_id).first()
    data = request.get_json()
    if not business:
        return jsonify({'message':'Business not found'})
    if not validate_review_title(data['review_title']):
        error = {'Review title error': 'Review title can only contain '+
            'alphanumeric, spaces and commas with characters between 2-100'}
        review_error.append(error)
    if not validate_review_text(data['review_text']):
        error = {'Review text error': 'Review text can only contain '+
            'alphanumeric, spaces, periods, underscores and commas '+
            'with characters between 2-100'}
        review_error.append(error)
    if review_error:
        return jsonify({'review validation error' : review_error})
    new_review = Review(rev_user_id=current_user.id, business_id=business_id,
                        review_title=data['review_title'],
                        review_text=data['review_text'])
    # Save to the database
    try:
        db.session.add(new_review)
        db.session.commit()
        return jsonify({'message': 'Review posted successfully'})
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify(str(error))

@busn.route('/businesses/<business_id>/reviews', methods=['GET'])
def get_reviews_for_business(business_id):
    """Get all reviews for a business"""
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=5, type=int)
    business = Business.query.filter_by(id=business_id).first()
    if not business:
        return jsonify({'message':'Business not found'})
    reviews = business.reviews.paginate(page, limit, error_out=False).items
    output = []
    # Get review data into a list of dictionaries
    for review in reviews:
        review_data = {}
        review_data['review_title'] = review.review_title
        review_data['review_text'] = review.review_text
        review_data['date_reviewed'] = review.date_reviewed
        output.append(review_data)
    return jsonify({'reviews' : output})
    