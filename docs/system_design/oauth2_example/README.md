# OAuth 2.0 Authorization Code Flow Example

This is a complete, runnable example of the OAuth 2.0 Authorization Code flow using Python and FastAPI. It simulates the interaction between three separate parties:

1. **Authorization Server** (`auth_server.py`): Issues tokens.
2. **Resource Server** (`resource_server.py`): Protects data.
3. **Client Application** (`client_app.py`): Wants access to the data.

## Prerequisites

- Python 3.8+
- Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

## How to Run

You will need to run three separate processes (terminal windows).

### 1. Start the Authorization Server

Runs on port **8000**.

```bash
python auth_server.py
```

### 2. Start the Client Application

Runs on port **8001**.

```bash
python client_app.py
```

### 3. Start the Resource Server

Runs on port **8002**.

```bash
python resource_server.py
```

## Testing the Flow

1. Open your browser and go to the **Client App**: [http://localhost:8001](http://localhost:8001).
2. Click **"Login with OAuth2"**.
3. You will be redirected to the **Authorization Server** (port 8000).
4. Login with the mock credentials:
    - **Username**: `user`
    - **Password**: `password`
5. After logging in, you will be redirected back to the **Client App**.
6. The Client App will automatically:
    - Exchange the `code` for an `access_token`.
    - Use the token to fetch data from the **Resource Server** (port 8002).
7. You should see a generic greeting, the access token, and the secret message from the Resource Server.

## Key Concepts Demonstrated

- **Redirection**: How the user moves between Client and Auth Server.
- **State Parameter**: Used (rudimentarily) to secure the redirect.
- **Authorization Code**: The temporary credential exchanged for a token.
- **Access Token**: The Bearer token used for API access.
- **Introspection**: How the Resource Server validates the token with the Auth Server.
