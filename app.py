from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# In-memory database
# Passwords are: adminpassword, userpassword
users = [
    {'id': 1, 'username': 'admin', 'password': bcrypt.generate_password_hash('adminpassword').decode('utf-8'), 'role': 'admin'},
    {'id': 2, 'username': 'user', 'password': bcrypt.generate_password_hash('userpassword').decode('utf-8'), 'role': 'user'}
]

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['id'])
        self.username = user_data['username']
        self.role = user_data['role']

@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_id(int(user_id))
    if user_data:
        return User(user_data)
    return None

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
        if not current_user.is_authenticated or current_user.role != 'admin':
            return "Forbidden", 403
        return f(*args, **kwargs)
    return decorated_function

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
            user = User(user_data)
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/users', methods=['GET', 'POST'])
@login_required
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
