import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Header
import requests

app = FastAPI(title="Resource Server")

AUTH_SERVER_INTROSPECT_URL = "http://localhost:8000/introspect"

async def verify_token(authorization: str = Header(...)):
    """
    Dependency to validate the Bearer token.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header format")
    
    token = authorization.split(" ")[1]
    
    # Introspect token with Auth Server
    try:
        response = requests.post(AUTH_SERVER_INTROSPECT_URL, data={"token": token})
        if response.status_code != 200:
             raise HTTPException(status_code=401, detail="Token validation failed")
        
        token_data = response.json()
        if not token_data.get("active"):
            raise HTTPException(status_code=401, detail="Token is inactive or invalid")
            
        return token_data
    except Exception as e:
        print(f"Introspection error: {e}")
        raise HTTPException(status_code=401, detail="Token validation error")

@app.get("/protected")
def protected_resource(token_data: dict = Depends(verify_token)):
    """
    A protected endpoint that returns data only if a valid token is present.
    """
    return {
        "message": "This is secret data from the Resource Server!",
        "owner": token_data.get("username"),
        "client": token_data.get("client_id")
    }

if __name__ == "__main__":
    print("Running Resource Server on http://localhost:8002")
    uvicorn.run(app, host="127.0.0.1", port=8002)
