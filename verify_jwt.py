import jwt
from flask import Flask

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MzcyNTc5OCwianRpIjoiY2U5OTM1MDQtYTVkNS00MGVlLTgzNDAtYjcwOWMxNzFkYTY3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIiLCJuYmYiOjE3NjM3MjU3OTgsImV4cCI6MTc2MzcyNjY5OH0.rUdtxpZHZryEebb5SnbzIY53keym_mSrUWmqpZWJxQg"

try:
    decoded = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
    print("Signature Verified!")
    print(decoded)
except Exception as e:
    print(f"Verification Failed: {e}")
