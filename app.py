from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, set_access_cookies, 
    set_refresh_cookies, unset_jwt_cookies, decode_token
)
from flask_bcrypt import Bcrypt
from functools import wraps
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'  # Change this!
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Disabled for simplicity in this demo
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# In-memory database
# Passwords are: adminpassword, userpassword
users = [
    {'id': 1, 'username': 'admin', 'password': bcrypt.generate_password_hash('adminpassword').decode('utf-8'), 'role': 'admin'},
    {'id': 2, 'username': 'user', 'password': bcrypt.generate_password_hash('userpassword').decode('utf-8'), 'role': 'user'}
]

def get_user(username):
    for user in users:
        if user['username'] == username:
            return user
    return None

def get_user_by_id(user_id):
    for user in users:
        if user['id'] == user_id:
            return user
    return None

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_username = get_jwt_identity()
        user = get_user(current_username)
        if not user or user['role'] != 'admin':
            return "Forbidden", 403
        return f(*args, **kwargs)
    return decorated_function

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    refresh_token = request.cookies.get('refresh_token_cookie')
    if refresh_token:
        try:
            decoded_token = decode_token(refresh_token)
            identity = decoded_token['sub']
            access_token = create_access_token(identity=identity)
            resp = make_response(redirect(request.url))
            set_access_cookies(resp, access_token)
            return resp
        except Exception:
            pass
    
    flash('Session expired, please login again.')
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = get_user(username)
        if user_data and bcrypt.check_password_hash(user_data['password'], password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            resp = make_response(redirect(url_for('dashboard')))
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    unset_jwt_cookies(resp)
    return resp

@app.route('/dashboard')
@jwt_required()
def dashboard():
    current_username = get_jwt_identity()
    user = get_user(current_username)
    return render_template('dashboard.html', user=user)

@app.route('/profile')
@jwt_required()
def profile():
    current_username = get_jwt_identity()
    user = get_user(current_username)
    return render_template('profile.html', user=user)

@app.route('/users', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def users_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_id = max([u['id'] for u in users]) + 1 if users else 1
        users.append({'id': new_id, 'username': username, 'password': hashed_password, 'role': role})
        return redirect(url_for('users_page'))
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
