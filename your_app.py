# your_app.py

from google.cloud import bigquery
from google.api_core.exceptions import Conflict

DATASET_ID = 'python_big_query'
TABLE_ID = 'python_login'
SCHEMA = [
    bigquery.SchemaField('user_id', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('email', 'STRING', mode='REQUIRED'),
]

# Mock the BigQuery client and table reference for testing
class MockBigQueryClient:
    def __init__(self):
        self.dataset = MagicMock()

    def dataset(self, dataset_id):
        return self.dataset

    def table(self, table_id):
        return MagicMock()

class MockTableReference:
    def __init__(self):
        self.schema = SCHEMA

class MockConflict(Exception):
    pass

# Mock the BigQuery client and table reference for testing
bigquery_client = MockBigQueryClient()
table_reference = MockTableReference()

try:
    # Attempt to create a table
    bigquery_client.create_table(table_reference)
except MockConflict:
    pass

def check_user_exists(user_id, email):
    # Implement logic to check if user exists in BigQuery
    query = f"SELECT * FROM `{DATASET_ID}.{TABLE_ID}` WHERE user_id = '{user_id}' OR email = '{email}'"
    query_job = bigquery_client.query(query)
    return len(list(query_job)) > 0

def create_new_user(user_id, email):
    # Implement logic to create a new user in BigQuery
    row = {'user_id': user_id, 'email': email}
    bigquery_client.insert_rows_json(table_reference, [row])

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
