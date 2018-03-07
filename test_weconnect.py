import os
import unittest
import json
from app import create_app

class TestAuthentication(unittest.TestCase):
    """Class to test API authentication"""

    def setUp(self):
        self.app = create_app(config_name="testing")
        create_app.testing = True
        current_user = "1"
        self.client = self.app.test_client
        self.login_user = {"username" : "test_user", "password" : "Test123"}
        self.test_user = {"username" : "test_user", "password" : "Test123"}
        self.test_business = {"name" : "Andela Kenya", 
                                "user_id": current_user,
                                "location" : "Nairobi, Kenya", 
                                "web_address" : "www.andela.com", 
                                "category" : "IT"}
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
            data=json.dumps(self.test_user), 
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created', str(response.data))

    def test_get_users(self):
        """Test api can get all users"""
        response = self.client().get('/api/v1/auth/users')
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        """Test api can login registered user"""
        self.client().post('/api/v1/auth/login', 
            data=json.dumps(self.test_user), 
            headers={'content-type':'application/json', 
                    'x-access-token':self.token})
        response = self.client().post('/api/v1/auth/login', 
            data=json.dumps(self.test_user), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_register_business(self):
        """Test api can register new business"""
        response = self.client().post('/api/v1/businesses', 
            data=json.dumps(self.test_business), 
            headers={'content-type':'application/json', 
                    'x-access-token':self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Business created', str(response.data))

    def test_get_businesses(self):
        """Test api can get all businesses"""
        response = self.client().get('/api/v1/businesses')
        self.assertEqual(response.status_code, 200)

    def test_get_one_business(self):
        """Test api can get one business"""
        response = self.client().get('/api/v1/business/2')
        
    

if __name__ == "__main__":
    unittest.main()