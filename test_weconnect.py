import os
import unittest
import json
from app import create_app

from app.models import User, Business, Review

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
        self.reset_user = {"username" : "reset_user", "password" : "Reset123", 
                    "name": "Reset User", "email":"reset_user@weconnect.com", 
                    "confirm_password" : "Reset123"}
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
        self.token = json.loads(to_response.data.decode())
        token = self.token['token']

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
            data=json.dumps(self.test_user), 
            content_type='application/json')
        dup_response = self.client().post('/api/v1/auth/register', 
            data=json.dumps(self.test_user), 
            content_type='application/json')
        self.assertIn('Username already exists', str(dup_response.data))

    def test_get_users(self):
        """Test api can get all users"""
        response = self.client().get('/api/v1/auth/users')
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        """Test api can login registered user"""
        self.client().post('/api/v1/auth/register', 
            data=json.dumps(self.login_user), 
            headers={'content-type':'application/json'})
        response = self.client().post('/api/v1/auth/login', 
            data=json.dumps(self.login_user), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        """Test api can reset user password"""
        self.client().post('/api/v1/auth/register', 
            data=json.dumps(self.reset_user), 
            content_type='application/json')
        response = self.client().post('/api/v1/auth/reset-password', 
            data=json.dumps(self.reset_user), 
            content_type='application/json')
        self.reset_user['password'] = "ResetAgain12"
        self.assertEqual(response.status_code, 200)
        self.assertIn("Password reset successful", str(response.data))
        
    def test_logout_user(self):
        """Test api can logout user"""
        response = self.client().post('/api/v1/auth/logout', 
            data=json.dumps(self.login_user), content_type='application/json')
        self.assertIn("You are now logged out", str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_register_and_get_business(self):
        """Test api can register new business"""
        response = self.client().post('/api/v1/businesses', 
            data=json.dumps(self.test_business), 
            headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Business created', str(response.data))
        response_ = self.client().get('/api/v1/businesses/1')

        print(response_)
        self.assertEqual(response_.status_code, 200)

    def test_cannot_create_duplicate_business(self):
        """Test api cannot create duplicate business"""
        response = self.client().post('/api/v1/businesses', 
            data=json.dumps(self.test_business), 
            headers={'content-type':'application/json'})
        dup_response = self.client().post('/api/v1/businesses', 
            data=json.dumps(self.test_business), 
            headers={'content-type':'application/json'})
        self.assertIn("Business name already exists.", str(dup_response.data))

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
            headers={'content-type':'application/json'})
        response = self.client().put('/api/v1/businesses/1', 
            data=json.dumps(test_business), 
            headers={'content-type':'application/json'})
        test_business['name'] = "Google"
        test_business['location'] = "San Francisco, CA"
        self.assertEqual(response.status_code, 200)
        self.assertEqual(test_business['name'], "Google")
        
    def test_cannot_update_with_existing_business_name(self):
        pass
        
    def test_cannot_update_with_existing_web_address(self):
        pass

    def test_delete_one_business(self):
        """Test api can delete a business"""
        response = self.client().delete('/api/v1/businesses/1')
        self.assertEqual(response.status_code, 200)

    def test_user_can_post_review(self):
        """Test that a user can post a review for a business"""
        new_rev = {"review_title": "Test review", "review_text":"Lorem ipsum"}
        response = self.client().post('/api/v1/businesses/1/reviews', 
            data=json.dumps(new_rev), 
            headers={'content-type':'application/json'})
        self.assertIn("Review posted successfully", str(response.data))
        self.assertEqual(response.status_code, 200)
        view_response = self.client().get('/api/v1/businesses/1/reviews')
        self.assertEqual(view_response.status_code, 200)
        
    def test_cannot_create_duplicate_web_address(self):
        pass

    def tearDown(self):
        self.business_i.businesses.clear()
        self.test1_user.clear()
        self.reset_user.clear()
        self.login_user.clear()
        self.test_business.clear()
        self.review_business.clear() 

if __name__ == "__main__":
    unittest.main()