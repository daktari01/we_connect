import unittest

from app.v2.auth.views import validate_names, validate_email, \
    validate_password, validate_username
from app.v2.businesses.views import validate_business_name, \
    validate_web_address, validate_location, validate_category, \
    validate_review_title, validate_review_text

class TestRegex(unittest.TestCase):
    """Test the regular expression functions"""
    
    def test_validate_names(self):
        """Test that only valid names will be allowed"""
        correct_name = 'John'
        wrong_name = '[]@@99'
        self.assertTrue(validate_names(correct_name))
        self.assertFalse(validate_names(wrong_name))
        
    def test_validate_username(self):
        """Test that only valid usernames will be allowed"""
        correct_username = 'johnie'
        wrong_username = '    '
        self.assertTrue(validate_username(correct_username))
        self.assertFalse(validate_username(wrong_username))
        
    def test_validate_email(self):
        """Test that only valid emails will be allowed"""
        correct_email = 'johndoe@email.com'
        wrong_email = 'jondoe@email'
        self.assertTrue(validate_email(correct_email))
        self.assertFalse(validate_email(wrong_email))
        
    def test_validate_password(self):
        """Test that only valid passwords will be allowed"""
        correct_password = 'jonhie&929'
        wrong_password = 'jondoe'
        self.assertTrue(validate_password(correct_password))
        self.assertFalse(validate_password(wrong_password))
        
    def test_validate_business_name(self):
        """Test that only valid business names will be allowed"""
        correct_business_name = 'Google'
        wrong_business_name = '00'
        self.assertTrue(validate_business_name(correct_business_name))
        self.assertFalse(validate_business_name(wrong_business_name))
        
    def test_validate_web_address(self):
        """Test that only valid web addresses will be allowed"""
        correct_web_address = 'https://www.google.com'
        wrong_web_address = 'https://google.com'
        self.assertTrue(validate_web_address(correct_web_address))
        self.assertFalse(validate_web_address(wrong_web_address))
        
    def test_validate_location(self):
        """Test that only valid locations will be allowed"""
        correct_location = 'San Fransisco, CA'
        wrong_location = '{}Nairobi*'
        self.assertTrue(validate_location(correct_location))
        self.assertFalse(validate_location(wrong_location))
        
    def test_validate_category(self):
        """Test that only valid categories will be allowed"""
        correct_category = 'Telecommunication'
        wrong_category = '48292'
        self.assertTrue(validate_category(correct_category))
        self.assertFalse(validate_category(wrong_category))
        
    def test_validate_review_title(self):
        """Test that only valid review titles will be allowed"""
        correct_review_title = 'I like it'
        wrong_review_title = '   999  0+'
        self.assertTrue(validate_review_title(correct_review_title))
        self.assertFalse(validate_review_title(wrong_review_title))
        
    def test_validate_review_text(self):
        """Test that only valid review texts will be allowed"""
        correct_review_text = 'Lorem inpsum, dolor sit amet.'
        wrong_review_text = '((((((('
        self.assertTrue(validate_review_text(correct_review_text))
        self.assertFalse(validate_review_text(wrong_review_text))