import os
import unittest
import json
from app import create_app

class TestAuthentication(unittest.TestCase):
    """Class to test API authentication"""


    def setUp(self):
        self.app = create_app(config_name="testing")
        create_app.testing = True
        self.client = self.app.test_client
        self.test_user = {"username" : "test_user", "password" : "Test123"}
        self.test_business = {"name" : "Andela Kenya", 
                                "location" : "Nairobi, Kenya", 
                                "web_address" : "www.andela.com", 
                                "category" : "IT"}

    def test_register_user(self):
        """Test api can register new user"""
        response = self.client().post('/api/v1/auth/register', 
            data=json.dumps(self.test_user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created', str(response.data))

    def test_get_users(self):
        """Test api can get all users"""
        response = self.client().get('/api/v1/auth/users')
        self.assertEqual(response.status_code, 200)

    def test_register_business(self):
        """Test api can register new business"""
        response = self.client().post('/api/v1/businesses', 
            data=json.dumps(self.test_business), 
                content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Business created', str(response.data))

    def test_get_businesses(self):
        """Test api can get all businesses"""
        response = self.client().get('/api/v1/businesses')
        self.assertEqual(response.status_code, 200)
    

if __name__ == "__main__":
    unittest.main()