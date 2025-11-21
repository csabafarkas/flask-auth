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

## Authentication: JWT vs Sessions

This application uses **JSON Web Tokens (JWT)** for authentication, replacing the traditional server-side **Sessions**.

### How they differ

-   **Sessions**: The server creates a session ID and stores user data (like user ID) in memory or a database on the server. The session ID is sent to the client as a cookie. On every request, the server looks up the session ID to identify the user.
-   **JWT**: The server creates a signed token containing user data (claims) and sends it to the client (in this app, as a cookie). The server **does not** need to store this token. On every request, the server validates the token's signature to identify the user.

### Pros and Cons

| Feature | Sessions | JWT |
| :--- | :--- | :--- |
| **State** | **Stateful**: Server must store session data. | **Stateless**: Server doesn't store tokens (usually). |
| **Scalability** | Harder to scale horizontally (need shared session store like Redis). | **Easier to scale**: Any server can verify the token. |
| **Revocation** | Easy: Just delete the session from the server. | **Hard**: Tokens are valid until expiry. Requires blocklisting. |
| **Payload Size** | Small (just an ID). | Larger (contains data + signature). |
| **Client Support** | Browser only (Cookies). | Any client (Mobile, Browser, Server-to-Server). |

In this application, we store the JWT in a cookie (`access_token_cookie`) to maintain compatibility with the standard browser-based navigation and templates.

### Why Cookies?
We use **HttpOnly Cookies** instead of **Local Storage** for two main reasons:
1.  **Server-Side Rendering (SSR)**: Flask templates are rendered on the server. The server needs the token *during* the request to know if the user is logged in (e.g., to show "My Profile" vs "Login"). Cookies are automatically sent with every request, whereas Local Storage data must be sent manually via JavaScript (AJAX/Fetch), which doesn't work well with standard HTML navigation.
2.  **Security**: `HttpOnly` cookies cannot be accessed by JavaScript, which protects the token from Cross-Site Scripting (XSS) attacks.
