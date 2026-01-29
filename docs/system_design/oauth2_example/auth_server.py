import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
import uuid
import urllib.parse

app = FastAPI(title="Authorization Server")

# --- In-Memory Stores ---
AUTHORIZATION_CODES = {}
ACCESS_TOKENS = {}

# --- Registered Clients ---
CLIENTS = {
    "my-client-app": {
        "client_secret": "my-client-secret-123",
        "redirect_uris": ["http://localhost:8001/callback"]
    }
}

@app.get("/authorize", response_class=HTMLResponse)
async def authorize_page(client_id: str, redirect_uri: str, state: str = "", scope: str = ""):
    """
    1. Validate Client ID and Redirect URI.
    2. Show a login page to the user (resource owner).
    """
    if client_id not in CLIENTS:
        raise HTTPException(status_code=400, detail="Invalid Client ID")
    
    if redirect_uri not in CLIENTS[client_id]["redirect_uris"]:
        raise HTTPException(status_code=400, detail="Invalid Redirect URI")
    
    # Simple HTML login form
    return f"""
    <html>
        <head><title>Auth Server Login</title></head>
        <body style="font-family: sans-serif; padding: 20px;">
            <h2>Authorization Server</h2>
            <p>App <b>{client_id}</b> wants to access your data.</p>
            <form action="/authorize" method="post">
                <input type="hidden" name="client_id" value="{client_id}">
                <input type="hidden" name="redirect_uri" value="{redirect_uri}">
                <input type="hidden" name="state" value="{state}">
                <label>Username: <input type="text" name="username" value="user"></label><br><br>
                <label>Password: <input type="password" name="password" value="password"></label><br><br>
                <button type="submit" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none;">Allow Access</button>
            </form>
        </body>
    </html>
    """

@app.post("/authorize")
async def process_authorization(
    client_id: str = Form(...),
    redirect_uri: str = Form(...),
    state: str = Form(""),
    username: str = Form(...),
    password: str = Form(...)
):
    """
    3. User entered credentials. Validate them (mocked).
    4. Generate Authorization Code.
    5. Redirect back to Client with the Code.
    """
    # Mock authentication
    if username != "user" or password != "password":
        return HTMLResponse("Invalid credentials", status_code=401)

    # Validated! Generate Auth Code
    auth_code = str(uuid.uuid4())
    AUTHORIZATION_CODES[auth_code] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "username": username
    }

    # Redirect to client
    params = {"code": auth_code, "state": state}
    url = f"{redirect_uri}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url=url, status_code=303)


@app.post("/token")
async def issue_token(
    grant_type: str = Form(...),
    code: str = Form(...),
    redirect_uri: str = Form(...),
    client_id: str = Form(...),
    client_secret: str = Form(...)
):
    """
    6. Client exchanges Auth Code for Access Token.
    """
    if grant_type != "authorization_code":
        raise HTTPException(status_code=400, detail="Unsupported grant_type")
    
    if client_id not in CLIENTS or CLIENTS[client_id]["client_secret"] != client_secret:
        raise HTTPException(status_code=401, detail="Invalid Client Credentials")
    
    auth_data = AUTHORIZATION_CODES.get(code)
    if not auth_data:
        raise HTTPException(status_code=400, detail="Invalid or expired Authorization Code")
    
    if auth_data["redirect_uri"] != redirect_uri:
        raise HTTPException(status_code=400, detail="Redirect URI mismatch")

    # Generate Access Token
    access_token = str(uuid.uuid4())
    # In a real app, this would be a JWT or better opaque structure
    token_data = {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": "read_data"
    }
    
    # Store token (for the resource server to validate later - simpler if we share DB, or use JWT)
    # Since Resource Server is separate, normally we'd verify JWT or use introspection endpoint.
    # For this ONE-FILE mock setup, we can't easily share memory across processes.
    # TO SOLVE THIS: We will create an /introspect endpoint on THIS server,
    # and the Resource Server will call it.
    ACCESS_TOKENS[access_token] = {
        "client_id": client_id,
        "username": auth_data["username"],
        "active": True
    }
    
    # Burn the code (it's one-time use)
    del AUTHORIZATION_CODES[code]
    
    return token_data

@app.post("/introspect")
async def introspect_token(token: str = Form(...)):
    """
    Resource Server calls this to validate the token.
    RFC 7662
    """
    token_info = ACCESS_TOKENS.get(token)
    if not token_info:
        return {"active": False}
    return token_info

if __name__ == "__main__":
    print("Running Authorization Server on http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
