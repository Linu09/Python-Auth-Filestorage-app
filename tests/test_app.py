import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO
from flask import Flask, url_for  # Import url_for

from app import app, check_user_exists, create_new_user, upload_file_to_storage, allowed_file

class TestYourApplication(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_login_route_successful_login(self):
        # Mock the check_user_exists function to simulate a successful login
        with patch('app.check_user_exists', return_value=True):
            response = self.app.post('/login', data={'user_id': 'some_id', 'email': 'test@example.com', 'password': 'password'})
            self.assertEqual(response.status_code, 302)  # Redirects to profile

    def test_signup_route_duplicate_user(self):
        # Mock the check_user_exists function to simulate a duplicate user during signup
        with patch('app.check_user_exists', return_value=True):
            response = self.app.post('/signup', data={'user_id': 'some_id', 'email': 'test@example.com', 'password': 'password'})
            self.assertIn(b'User ID or email already exists', response.data)

    def test_profile_route_file_upload(self):
        # Mock the upload_file_to_storage function to simulate a successful file upload
        with patch('app.upload_file_to_storage', return_value=None):
            # Assuming the user is already logged in (you can mock the session data)
            # Use BytesIO to simulate file data
            file_data = (BytesIO(b'This is a test file content'), 'test.txt')
            response = self.app.post('/profile', data={'file': file_data}, content_type='multipart/form-data')

            # Check if the response is a redirect
            self.assertEqual(response.status_code, 302)

            # Use url_for to generate the correct URL for comparison
            expected_url = url_for('login')
            self.assertEqual(response.headers['Location'], expected_url)

    # You can similarly write tests for other routes and functions

if __name__ == '__main__':
    unittest.main()
