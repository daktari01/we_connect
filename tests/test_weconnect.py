import os
import unittest
import json
from app import create_app

from app.v1.models import User, Business, Review

class TestAuthentication(unittest.TestCase):
    """Class to test API authentication"""

    def setUp(self):
        self.app = create_app(config_name="testing")
        create_app.testing = True
        self.user = User()
        self.business_i = Business()
        current_user = "1"
        self.client = self.app.test_client
        self.test_user = {"username" : "test_user", "password" : "Test123", 
                        "name": "Test User", "email":"test_user@weconnect.com",
                         "confirm_password" : "Test123"}
        self.test1_user = {"username" : "test1_user", "password" : "Test123", 
                    "name": "Test User1", "email":"test_user1@weconnect.com", 
                    "confirm_password" : "Test123"}
        self.email_user = {"username" : "email_user", "password" : "Email123", 
                    "name": "Email User1", "email":"login_user@weconnect.com", 
                    "confirm_password" : "Email123"}
        self.reset_passw = {"old_password": "Test123",
                            "new_password": "New123",
                            "confirm_new_password": "New123"}
        self.login_user = {"username" : "login_user", "password" : "Log123", 
                    "name": "Login User", "email":"login_user@weconnect.com", 
                    "confirm_password" : "Log123"}
        self.test_business = {"name" : "Andela Kenya", 
                                "user_id": current_user,
                                "location" : "Nairobi, Kenya", 
                                "web_address" : "www.andela.com", 
                                "category" : "IT"}
        self.review_business = {"name" : "CocaCola", 
                                "user_id": current_user,
                                "location" : "Austin, TX", 
                                "web_address" : "www.cocacola.com", 
                                "category" : "Food"}
        self.client().post('/api/v1/auth/register', 
            data=json.dumps(self.login_user), 
            content_type='application/json')
        to_response = self.client().post('/api/v1/auth/login', 
            data=json.dumps(self.login_user), 
            headers={"content-type":'application/json'})
        data = json.loads(to_response.data.decode())
        self.token = data['token']

    def test_register_user(self):
        """Test api can register new user"""
        response = self.client().post('/api/v1/auth/register', 
            data=json.dumps(self.test1_user), 
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', str(response.data))

    def test_cannot_create_duplicate_user(self):
        """Test api cannot create duplicate user"""
        response = self.client().post('/api/v1/auth/register', 
            data=json.dumps(self.login_user), 
            content_type='application/json')
        self.assertIn('Username already exists', str(response.data))

    def test_cannot_create_with_duplicate_email(self):
        """Test api cannot register user with duplicate email"""
        response = self.client().post('/api/v1/auth/register', 
            data=json.dumps(self.email_user), 
            content_type='application/json')
        self.assertIn('Email already exists. Try another one', 
            str(response.data))

    def test_get_users(self):
        """Test api can get all users"""
        response = self.client().get('/api/v1/auth/users', 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        """Test api can login registered user"""
        self.client().post('/api/v1/auth/register', 
            data=json.dumps(self.test_user), 
            headers={'content-type':'application/json'})
        response = self.client().post('/api/v1/auth/login', 
            data=json.dumps(self.test_user), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        """Test api can reset user password"""
        self.client().post('/api/v1/auth/register', 
            data=json.dumps(self.login_user), 
            headers={'content-type':'application/json'})
        self.client().post('/api/v1/auth/login', 
            data=json.dumps(self.login_user), content_type='application/json')
        response = self.client().post('/api/v1/auth/reset-password', 
            data=json.dumps(self.reset_passw), 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        self.assertEqual(response.status_code, 200)
        
    def test_logout_user(self):
        """Test api can logout user"""
        response = self.client().post('/api/v1/auth/logout', 
            data=json.dumps(self.login_user), 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        self.assertIn("You are now logged out", str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_register_and_get_a_business(self):
        """Test api can register new business"""
        self.client().post('/api/v1/auth/register', 
            data=json.dumps(self.login_user), 
            headers={'content-type':'application/json'})
        token_response = self.client().post('/api/v1/auth/login', 
            data=json.dumps(self.login_user), content_type='application/json')
        data = json.loads(token_response.data.decode())
        token = data['token']
        response = self.client().post('/api/v1/businesses', 
            data=json.dumps(self.test_business), 
            headers={'content-type':'application/json', 
                'x-access-token':token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Business created', str(response.data))
        response_ = self.client().get('/api/v1/businesses/1', 
            headers={'content-type':'application/json', 
                'x-access-token':token})
        self.assertEqual(response_.status_code, 200)

    def test_cannot_create_duplicate_business(self):
        """Test api cannot create duplicate business"""
        response = self.client().post('/api/v1/businesses', 
            data=json.dumps(self.test_business), 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        dup_response = self.client().post('/api/v1/businesses', 
            data=json.dumps(self.test_business), 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        self.assertIn("Web address already exists.", str(dup_response.data))

    def test_get_businesses(self):
        """Test api can get all businesses"""
        response = self.client().get('/api/v1/businesses')
        self.assertEqual(response.status_code, 200)

    def test_update_one_business(self):
        """Test api can update a business"""
        test_business = {"name" : "Andela Kenya", 
                                "user_id": "1",
                                "location" : "Nairobi, Kenya", 
                                "web_address" : "www.andela.com", 
                                "category" : "IT"}
        self.client().post('/api/v1/businesses', 
            data=json.dumps(test_business), 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        self.client().put('/api/v1/businesses/1', 
            data=json.dumps(test_business), 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        test_business['name'] = "Google"
        test_business['location'] = "San Francisco, CA"
        self.assertEqual(test_business['location'], "San Francisco, CA")
        self.assertEqual(test_business['name'], "Google")
        
    def test_cannot_update_with_existing_business_name(self):
        """Test api cannot update business with duplicate business name"""
        test_business = {"name" : "Andela Kenya", 
                                "user_id": "1",
                                "location" : "Nairobi, Kenya", 
                                "web_address" : "www.andela.com", 
                                "category" : "IT"}
        self.client().post('/api/v1/businesses', 
            data=json.dumps(test_business), 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        response = self.client().put('/api/v1/businesses/1', 
            data=json.dumps(test_business), 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        test_business['name'] = "Andela Kenya"
        self.assertIn('Business name already exists', str(response.data))
        
    def test_cannot_update_with_existing_web_address(self):
        """
        Test api cannot update business with duplicate business web address
        """
        test_business = {"name" : "Armco Kenya", 
                                "user_id": "1",
                                "location" : "Nakuru, Kenya", 
                                "web_address" : "www.andela.com", 
                                "category" : "Insurance"}

        self.client().post('/api/v1/businesses', 
            data=json.dumps(test_business), 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        response = self.client().put('/api/v1/businesses/1', 
            data=json.dumps(test_business), 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        test_business['web_address'] = "www.andela.com"
        self.assertIn('Web address already exists', str(response.data))

    def test_delete_one_business(self):
        """Test api can delete a business"""
        test_business = {"name" : "Armco Kenya", 
                                "user_id": "1",
                                "location" : "Nakuru, Kenya", 
                                "web_address" : "www.andela.com", 
                                "category" : "Insurance"}
        self.client().post('/api/v1/businesses', 
            data=json.dumps(test_business), 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        response = self.client().delete('/api/v1/businesses/1', 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        self.assertEqual(response.status_code, 200)

    def test_user_can_post_review(self):
        """Test that a user can post and get a review for a business"""
        test_business = {"name" : "Armco Kenya", 
                                "user_id": "1",
                                "location" : "Nakuru, Kenya", 
                                "web_address" : "www.andela.com", 
                                "category" : "Insurance"}
        self.client().post('/api/v1/businesses', 
            data=json.dumps(test_business), 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        new_rev = {"review_title": "Test review", "review_text":"Lorem ipsum"}
        response = self.client().post('/api/v1/businesses/1/reviews', 
            data=json.dumps(new_rev), 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        self.assertIn("Review posted successfully", str(response.data))
        self.assertEqual(response.status_code, 200)
        view_response = self.client().get('/api/v1/businesses/1/reviews', 
            headers={'content-type':'application/json', 
                'x-access-token':self.token})
        self.assertEqual(view_response.status_code, 200)

    def tearDown(self):
        self.business_i.businesses.clear()
        self.test1_user.clear()
        self.login_user.clear()
        self.test_business.clear()
        self.review_business.clear() 

if __name__ == "__main__":
    unittest.main()