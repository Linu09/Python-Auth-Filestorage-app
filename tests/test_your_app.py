import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from your_app import app, check_user_exists, create_new_user, allowed_file

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_check_user_exists(self):
        # Mock the BigQuery client and response
        with patch('your_app.bigquery_client.query') as mock_query:
            # Assume a user with ID 'test_user' and email 'test@example.com' exists
            mock_query.return_value = MagicMock(items=[{'user_id': 'test_user', 'email': 'test@example.com'}])
            result = check_user_exists('test_user', 'test@example.com')
            self.assertTrue(result)

            # Test a case where the user doesn't exist
            mock_query.return_value = MagicMock(items=[])
            result = check_user_exists('nonexistent_user', 'test@example.com')
            self.assertFalse(result)

    def test_create_new_user(self):
        # Mock the BigQuery client
        with patch('your_app.bigquery_client.insert_rows_json') as mock_insert_rows:
            create_new_user('new_user', 'new@example.com')
            # Ensure the insert_rows_json method is called with the expected arguments
            mock_insert_rows.assert_called_once_with(app.config['TABLE_REF'], [{'user_id': 'new_user', 'email': 'new@example.com'}])

    def test_allowed_file(self):
        # Test allowed file types
        self.assertTrue(allowed_file('test.txt'))
        self.assertTrue(allowed_file('test.pdf'))
        self.assertTrue(allowed_file('test.png'))

        # Test disallowed file types
        self.assertFalse(allowed_file('test.doc'))
        self.assertFalse(allowed_file('test.exe'))
        self.assertFalse(allowed_file('test.html'))

if __name__ == '__main__':
    unittest.main()
