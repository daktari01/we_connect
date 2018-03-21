import os
import unittest
import json

from v2 import db, create_app_v2

class TestWeconnect(unittest.TestCase):
    """Class that contains tests for the version 2 of WeConnect"""

    def setUp(self):
        """Initaliaze variables to be used in testing"""
        self.app = create_app_v2(config_name="testing")
        self.client = self.app.test_client()
        self.test_user = {"username":"morris", "first_name" : "Morris",
            "last_name" : "Maluni", "email":"maluni@weconnect.com",
            "first_password":"maluni123", "confirm_password":"maluni123"}
        self.test_login = {"username":"morris", "password":"maluni123"}
        self.reset_password = {"old_password": "maluni123",
                                "new_password": "maluni456",
                                "confirm_new_password": "maluni456"}
        self.test_business = {"name":"Andela", "location":"Nairobi, Kenya",
                                "category": "Software development",
                                "web_address":"www.andela.com"}

        with self.app.app_context():
            # Create all tables
            db.create_all()

    def test_user_can_register(self):
        """Test user can be registered into the system"""
        response = self.client().post('/api/v2/auth/register', 
                    data=json.dumps(self.test_user), 
                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', str(response.data))

    def test_user_can_login(self):
        """Test that a registered user can log in"""
        self.client().post('/api/v2/auth/login', 
                    data=json.dumps(self.test_login), 
                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
    def test_user_can_reset_password(self):
        """Test that a logged in user can reset own password"""
        response = self.client().post('/api/v2/auth/register', 
                    data=json.dumps(self.reset_password), 
                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
    def test_user_can_logout(self):
        """Test that user can log out"""
        pass
    
    def test_user_can_register_business(self):
        """Test that user can register a business"""
        response = self.client().post('/api/v2/auth/businesses', 
                    data=json.dumps(self.test_business), 
                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Business registered successfully', str(response.data))
    
    def test_user_can_get_all_businesses(self):
        """Test that user can get all businesses"""
        response = self.client().get('/api/v2/auth/businesses', 
                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_can_get_one_business(self):
        """Test that a user can get one business by id"""
        response = self.client().get('/api/v2/auth/businesses/1', 
                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_can_edit_business(self):
        """Test that a user can edit a business"""
        self.client().put('/api/v2/auth/businesses/1', 
                    content_type='application/json')
        self.test_business = {"name":"Google", "location":"San Francisco, CA",
                                "category": "Web services",
                                "web_address":"www.google.com"}
        self.assertEqual(self.test_business["name"], "Google")
        self.assertEqual(self.test_business["web_address"], "www.google.com")
        
    def tearDown(self):
        """Destroy all initialized variables"""
        with self.app.app_context():
            # destroy all tables
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()