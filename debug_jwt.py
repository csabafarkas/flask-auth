from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

with app.app_context():
    token = create_access_token(identity='testuser')
    print(f"Token: {token}")
    parts = token.split('.')
    print(f"Parts count: {len(parts)}")
    print(f"Header: {parts[0]}")
    print(f"Payload: {parts[1]}")
    print(f"Signature: {parts[2]}")
