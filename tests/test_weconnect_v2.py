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

    def tearDown(self):
        """Destroy all initialized variables"""
        with self.app.app_context():
            # destroy all tables
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()