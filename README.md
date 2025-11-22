# Flask Auth App

## Setup

1.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```
2.  Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the App

1.  Run the application:
    ```bash
    python app.py
    ```
2.  Open your browser and navigate to `http://127.0.0.1:5000`.

## Authentication

This application uses **Server-Side Sessions** for authentication.

-   **Sessions**: The server creates a session ID and stores user data (like user ID) in a secure cookie. On every request, the server looks up the session ID to identify the user.
-   **Security**: Passwords are hashed using `Flask-Bcrypt`.
