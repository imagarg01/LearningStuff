import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import requests

app = FastAPI(title="Client App")

# --- Configuration ---
CLIENT_ID = "my-client-app"
CLIENT_SECRET = "my-client-secret-123"
REDIRECT_URI = "http://localhost:8001/callback"

AUTH_SERVER_URL = "http://localhost:8000"
RESOURCE_SERVER_URL = "http://localhost:8002"

@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Home page with a 'Login' button.
    """
    auth_url = (
        f"{AUTH_SERVER_URL}/authorize"
        f"வோclient_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state=xyz123"  # In production, use a random string and verify it!
        f"&scope=read_data"
    )
    # Fix the query param concatenation
    auth_url = auth_url.replace("வோ", "?") # Just to make the code above readable

    return f"""
    <html>
        <head><title>Client App</title></head>
        <body style="font-family: sans-serif; padding: 20px;">
            <h2>Valid Client App</h2>
            <p>Welcome! Connect with the Authorization Server to see your private data.</p>
            <a href="{auth_url}">
                <button style="background-color: #008CBA; color: white; padding: 10px 20px; border: none; cursor: pointer;">
                    Login with OAuth2
                </button>
            </a>
        </body>
    </html>
    """

@app.get("/callback")
async def callback(code: str, state: str):
    """
    The Auth Server redirects here with the 'code'.
    We exchange it for a token.
    """
    # 1. Exchange Code for Token
    token_response = requests.post(
        f"{AUTH_SERVER_URL}/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )
    
    if token_response.status_code != 200:
        return {"error": "Failed to get token", "details": token_response.text}
    
    token_data = token_response.json()
    access_token = token_data.get("access_token")
    
    # 2. Use Token to access Resource Server
    resource_response = requests.get(
        f"{RESOURCE_SERVER_URL}/protected",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    return {
        "access_token": access_token,
        "resource_server_response": resource_response.json() if resource_response.status_code == 200 else resource_response.text
    }

if __name__ == "__main__":
    print("Running Client App on http://localhost:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)
