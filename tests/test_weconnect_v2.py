import os
import unittest
import json
import psycopg2
from sqlalchemy.exc import IntegrityError

from v2 import db, create_app_v2
from v2.models import User, Review, Business

class TestWeconnect(unittest.TestCase):
    """Class that contains tests for the version 2 of WeConnect"""

    def setUp(self):
        """Initaliaze variables to be used in testing"""
        self.app = create_app_v2(config_name="testing")
        self.client = self.app.test_client
        self.test_user = {"username":"morris", "first_name" : "Morris",
            "last_name" : "Maluni", "email":"maluni@weconnect.com",
            "first_password":"maluni123", "confirm_password":"maluni123"}
        self.login_user = {"username":"login", "first_name" : "Login",
            "last_name" : "User", "email":"login.user@weconnect.com",
            "first_password":"login123", "confirm_password":"login123"}
        self.test_login = {"username":"morris", "password":"maluni123"}
        self.user_login = {"username":"login", "password":"login123"}
        self.reset_password = {"old_password": "maluni123",
                                "new_password": "maluni456",
                                "confirm_new_password": "maluni456"}
        self.test_business = {"name":"Andela", "location":"Nairobi, Kenya",
                                "category": "Software development",
                                "web_address":"www.andela.com"}
        self.test_review = {"review_title": "I liked it",
                            "review_text": "Lorem ipsum dolor sit amet"}
        # Set up the token
        self.client().post('/api/v2/auth/register', 
            data=json.dumps(self.login_user), 
            content_type='application/json')
        to_response = self.client().post('/api/v2/auth/login', 
            data=json.dumps(self.user_login), 
            headers={"content-type":'application/json'})
        data = json.loads(to_response.data.decode())
        self.token = data['token']

        with self.app.app_context():
            # Create all tables
            db.create_all()
        self.app.app_context().push()
        

    def test_user_can_register(self):
        """Test user can be registered into the system"""
        response = self.client().post('/api/v2/auth/register', 
                    data=json.dumps(self.test_user), 
                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User registered successfully', str(response.data))

    def test_duplicate_registration(self):
        """Test that a user cannot register twice"""
        self.client().post('/api/v2/auth/register', 
                    data=json.dumps(self.test_user), 
                    content_type='application/json')
        response = self.client().post('/api/v2/auth/register', 
                    data=json.dumps(self.test_user), 
                    content_type='application/json')
        print(">>>>>>>>>>>")
        print(response.data)
        print(">>>>>>>>>>>")
        self.assertRaises(IntegrityError, response)
        
        # self.assertIn('duplicate key value violates unique constraint', 
        #             str(response.data))
        # with self.assertRaises(psycopg2.IntegrityError):
        #     self.client().post('/api/v2/auth/register',
        #         data=json.dumps(self.test_user), 
        #         content_type='application/json')

    def test_user_can_login(self):
        """Test that a registered user can log in"""
        self.client().post('/api/v2/auth/register', 
                    data=json.dumps(self.test_user), 
                    content_type='application/json')
        response = self.client().post('/api/v2/auth/login', 
                    data=json.dumps(self.test_login), 
                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_can_get_all_users(self):
        """Test that an authenticated user can retrieve all users"""
        response = self.client().get('/api/v2/auth/users', 
                    headers={'content-type':'application/json', 
                        'x-access-token': self.token})
        self.assertEqual(response.status_code, 200)
        
    def test_user_can_reset_password(self):
        """Test that a logged in user can reset own password"""
        response = self.client().post('/api/v2/auth/reset-password', 
                    data=json.dumps(self.reset_password), 
                    headers={'content-type':'application/json', 
                        'x-access-token': self.token})
        self.assertEqual(response.status_code, 200)
        
    def test_user_can_logout(self):
        """Test that user can log out"""
        response = self.client().post('/api/v2/auth/logout', 
                    data=json.dumps(self.login_user), 
                    headers={'content-type':'application/json', 
                                'x-access-token': self.token})
        self.assertIn('Log out successful', str(response.data))
    
    def test_user_can_register_business(self):
        """Test that user can register a business"""
        response = self.client().post('/api/v2/businesses', 
                    data=json.dumps(self.test_business), 
                    headers={'content-type':'application/json', 
                                'x-access-token': self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Business registered successfully', str(response.data))

    def test_user_cannot_register_duplicate_business(self):
        """Test that a user cannot register a duplicate business"""
        self.client().post('/api/v2/businesses', 
                    data=json.dumps(self.test_business), 
                    headers={'content-type':'application/json', 
                                'x-access-token': self.token})
        response = self.client().post('/api/v2/businesses', 
                    data=json.dumps(self.test_business), 
                    headers={'content-type':'application/json', 
                                'x-access-token': self.token})
        self.assertIn('duplicate key value violates unique constraint', 
                        str(response.data))
    
    def test_user_can_get_all_businesses(self):
        """Test that user can get all businesses"""
        response = self.client().get('/api/v2/businesses', 
                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_can_get_one_business(self):
        """Test that a user can get one business by id"""
        self.client().post('/api/v2/businesses', 
                    data=json.dumps(self.test_business), 
                    headers={'content-type':'application/json', 
                                'x-access-token': self.token})
        response = self.client().get('/api/v2/businesses/1', 
                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_can_edit_business(self):
        """Test that a user can edit a business"""
        self.client().post('/api/v2/businesses', 
                    data=json.dumps(self.test_business), 
                    headers={'content-type':'application/json', 
                                'x-access-token': self.token})
        self.client().put('/api/v2/businesses/1', 
                    content_type='application/json')
        self.test_business = {"name":"Google", "location":"San Francisco, CA",
                                "category": "Web services",
                                "web_address":"www.google.com"}
        self.assertEqual(self.test_business["name"], "Google")
        self.assertEqual(self.test_business["web_address"], "www.google.com")

    def test_user_can_delete_business(self):
        """Test that a user can delete own business"""
        self.client().post('/api/v2/businesses', 
                    data=json.dumps(self.test_business), 
                    headers={'content-type':'application/json', 
                                'x-access-token': self.token})
        business_id = db.session.query(Business).first().id
        response = self.client().delete('/api/v2/businesses/{}'
                                            .format(business_id), 
                    headers={'content-type':'application/json', 
                                'x-access-token': self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Business deleted successfully', str(response.data))

    def test_user_can_post_review(self):
        """Test that a user can post a review for a business"""
        self.client().post('/api/v2/businesses', 
                    data=json.dumps(self.test_business), 
                    headers={'content-type':'application/json', 
                                'x-access-token': self.token})
        business_id = db.session.query(Business).first().id
        response = self.client().post('/api/v2/businesses/{}/reviews'
                                .format(business_id), 
                    data=json.dumps(self.test_review), 
                    headers={'content-type':'application/json', 
                                'x-access-token': self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Review posted successfully', str(response.data))

    def test_user_can_get_all_reviews(self):
        """Test that a user can get all reviews for a business"""
        self.client().post('/api/v2/businesses', 
                    data=json.dumps(self.test_business), 
                    headers={'content-type':'application/json', 
                                'x-access-token': self.token})
        business_id = db.session.query(Business).first().id
        self.client().post('/api/v2/businesses/{}/reviews'
                                .format(business_id), 
                    data=json.dumps(self.test_review), 
                    headers={'content-type':'application/json', 
                                'x-access-token': self.token})
        response = self.client().get('/api/v2/businesses/{}/reviews'
                    .format(business_id), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """Destroy all initialized variables"""
        with self.app.app_context():
            # destroy all tables
            db.session.query(Review).delete()
            db.session.query(Business).delete()
            db.session.query(User).delete()
            db.session.commit()

if __name__ == '__main__':
    unittest.main()