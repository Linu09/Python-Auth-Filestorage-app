# tests/test_app.py
import unittest
from unittest.mock import patch
from your_app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Index Page', response.data)

    @patch('your_app.check_user_exists', return_value=True)
    def test_login_successful(self, mock_check_user_exists):
        response = self.app.post('/login', data={'user_id': 'test_user', 'email': 'test@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Should redirect to profile on successful login

    @patch('your_app.check_user_exists', return_value=False)
    def test_login_unsuccessful(self, mock_check_user_exists):
        response = self.app.post('/login', data={'user_id': 'nonexistent_user', 'email': 'nonexistent@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Should redirect to signup if login is unsuccessful

    @patch('your_app.check_user_exists', return_value=False)
    def test_signup_successful(self, mock_check_user_exists):
        response = self.app.post('/signup', data={'user_id': 'new_user', 'email': 'new@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Should redirect to login on successful signup

    @patch('your_app.check_user_exists', return_value=True)
    def test_signup_unsuccessful(self, mock_check_user_exists):
        response = self.app.post('/signup', data={'user_id': 'existing_user', 'email': 'existing@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 200)  # Should stay on signup page if signup is unsuccessful

    def test_profile_route_requires_login(self):
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 302)  # Should redirect to login if not logged in

    @patch('your_app.check_user_exists', return_value=True)
    def test_profile_route_with_login(self, mock_check_user_exists):
        with self.app.session_transaction() as session:
            session['user'] = {'user_id': 'test_user', 'email': 'test@example.com'}
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Profile Page', response.data)

if __name__ == '__main__':
    unittest.main()
