import requests
import time
import sys

BASE_URL = "http://127.0.0.1:5000"
LOGIN_URL = f"{BASE_URL}/login"
DASHBOARD_URL = f"{BASE_URL}/dashboard"

session = requests.Session()

# 1. Login
print("Logging in...")
response = session.post(LOGIN_URL, data={'username': 'user', 'password': 'userpassword'})
if response.status_code != 200:
    print("Login failed")
    sys.exit(1)

initial_access_token = session.cookies.get('access_token_cookie')
if not initial_access_token:
    print("No access token received")
    sys.exit(1)
print(f"Initial Access Token: {initial_access_token[:20]}...")

# 2. Wait for expiry
print("Waiting 16 seconds for token expiry...")
time.sleep(16)

# 3. Access Dashboard (should trigger refresh)
print("Accessing Dashboard...")
response = session.get(DASHBOARD_URL)

if response.status_code != 200:
    print(f"Dashboard access failed: {response.status_code}")
    # print(response.text)
    sys.exit(1)

new_access_token = session.cookies.get('access_token_cookie')
print(f"New Access Token:     {new_access_token[:20]}...")

if initial_access_token != new_access_token:
    print("SUCCESS: Access token was refreshed!")
else:
    print("FAILURE: Access token was NOT refreshed (or identical).")
    sys.exit(1)
