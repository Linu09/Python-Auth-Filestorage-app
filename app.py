from flask import Flask, render_template, request, redirect, url_for, session, flash
from google.cloud import storage, bigquery
from google.api_core.exceptions import Conflict
from werkzeug.utils import secure_filename

import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'default_credential_file.json')

app = Flask(__name__)
app.secret_key = 'xyz'

# Initialize GCP services
storage_client = storage.Client()
bigquery_client = bigquery.Client()

# Constants
BUCKET_NAME = os.getenv('BUCKET_NAME', 'default_bucket_name')
DATASET_ID = os.getenv('DATASET_ID', 'default_dataset_id')
TABLE_ID = os.getenv('TABLE_ID', 'default_table_id')
SCHEMA = [
    bigquery.SchemaField('user_id', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('email', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('password', 'STRING', mode='REQUIRED'),  # New password field
]
TABLE_REF = bigquery_client.dataset(DATASET_ID).table(TABLE_ID)
TABLE_REF.schema = SCHEMA

try:
    bigquery_client.create_table(TABLE_REF)
except Conflict:
    pass

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_storage(file, user_id, filename):
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"uploads/{user_id}/{filename}")
    blob.upload_from_file(file)


def get_user_files(user_id):
    bucket_name = 'login-intergated_page'
    prefix = f"uploads/{user_id}/"
    delimiter = '/'

    blobs = storage_client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    files = []
    for blob in blobs:
        if isinstance(blob, storage.Blob):
            # Extracting file name from the full path
            file_name = blob.name.replace(prefix, '')
            files.append(file_name)

    return files


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        email = request.form.get('email')
        password = request.form.get('password')  # New password field

        # Check if user exists
        user_exists = check_user_exists(user_id, email, password)

        if user_exists:
            # User exists, perform login
            session['user'] = {'user_id': user_id, 'email': email}
            return redirect(url_for('profile'))
        else:
            # User doesn't exist or password is incorrect, redirect to signup page
            return redirect(url_for('signup'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle user registration logic here
        user_id = request.form.get('user_id')
        email = request.form.get('email')
        password = request.form.get('password')  # New password field

        # Check if user ID and email are unique
        if not check_user_exists(user_id, email, password):
            # If unique, create a new user
            create_new_user(user_id, email, password)
            flash('Account created successfully!')
            return redirect(url_for('login'))
        else:
            # If not unique, show an error message
            flash('User ID or email already exists. Please choose unique values.', 'error')

    # Render the signup page
    return render_template('signup.html')

def check_user_exists(user_id, email, password):
    # Implement logic to check if user exists in BigQuery
    query = f"SELECT * FROM `{DATASET_ID}.{TABLE_ID}` WHERE user_id = '{user_id}' AND email = '{email}' AND password = '{password}'"
    query_job = bigquery_client.query(query)
    return len(list(query_job)) > 0

def create_new_user(user_id, email, password):
    # Implement logic to create a new user in BigQuery
    row = {'user_id': user_id, 'email': email, 'password': password}
    bigquery_client.insert_rows_json(TABLE_REF, [row])

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    user_files = get_user_files(user['user_id'])

    if request.method == 'POST':
        # File upload logic
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_file_to_storage(file, user['user_id'], filename)
            flash('File uploaded successfully!')

    return render_template('profile.html', user=user, user_files=user_files)

@app.route('/download/<filename>')
def download_file(filename):
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"uploads/{user['user_id']}/{filename}")

    # Generate a signed URL for file download
    download_url = blob.generate_signed_url(
        version='v4',
        expiration=300,  # URL expires in 5 minutes
        method='GET'
    )

    return redirect(download_url)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)%                            
