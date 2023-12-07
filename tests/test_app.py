import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO
from flask import Flask, url_for
from app import app, check_user_exists, create_new_user, upload_file_to_storage, allowed_file

class TestYourApplication(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_login_route_successful_login(self):
        with patch('app.check_user_exists', return_value=True):
            response = self.app.post('/login', data={'user_id': 'some_id', 'email': 'test@example.com', 'password': 'password'})
            self.assertEqual(response.status_code, 302)  # Redirects to profile

    def test_signup_route_duplicate_user(self):
        with patch('app.check_user_exists', return_value=True):
            response = self.app.post('/signup', data={'user_id': 'some_id', 'email': 'test@example.com', 'password': 'password'})
            self.assertIn(b'User ID or email already exists', response.data)

    def test_profile_route_file_upload(self):
        with patch('app.upload_file_to_storage', return_value=None):
            file_data = (BytesIO(b'This is a test file content'), 'test.txt')
            
            # Use test_request_context to create a temporary request context
            with app.test_request_context('/profile'):
                response = self.app.post('/profile', data={'file': file_data}, content_type='multipart/form-data')
                self.assertEqual(response.status_code, 302)
                
                # Use url_for within the request context to generate the correct URL for comparison
                expected_url = url_for('login')
                self.assertEqual(response.headers['Location'], expected_url)

if __name__ == '__main__':
    unittest.main()
