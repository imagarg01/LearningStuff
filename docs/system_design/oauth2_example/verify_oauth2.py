import subprocess
import time
import requests
import sys
import os
import signal

def run_server(script_name, port):
    print(f"Starting {script_name} on port {port}...")
    # Use sys.executable to ensure we use the same python environment
    process = subprocess.Popen(
        [sys.executable, script_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    return process

def test_flow():
    # 1. Start Servers
    auth_proc = run_server("auth_server.py", 8000)
    client_proc = run_server("client_app.py", 8001)
    resource_proc = run_server("resource_server.py", 8002)
    
    try:
        # Give them time to start
        time.sleep(5)
        
        # 2. Simulate User: POST /authorize to get code (Skip the GET login page)
        print("Simulating User Login...")
        login_data = {
            "client_id": "my-client-app",
            "redirect_uri": "http://localhost:8001/callback",
            "state": "xyz",
            "username": "user",
            "password": "password"
        }
        resp = requests.post("http://localhost:8000/authorize", data=login_data, allow_redirects=False)
        
        if resp.status_code != 303:
            print(f"Login failed: {resp.status_code} {resp.text}")
            return False
            
        redirect_url = resp.headers["Location"]
        print(f"Redirected to: {redirect_url}")
        
        # 3. Extract Code from URL
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(redirect_url)
        params = parse_qs(parsed_url.query)
        code = params["code"][0]
        state = params["state"][0]
        print(f"Got Auth Code: {code}")
        
        # 4. Simulate Browser redirecting to Client Callback
        # The client will then talk to Auth Server (token) and Resource Server (data)
        print("Visiting Client Callback...")
        callback_resp = requests.get(redirect_url)
        
        if callback_resp.status_code != 200:
             print(f"Callback failed: {callback_resp.status_code} {callback_resp.text}")
             return False
             
        data = callback_resp.json()
        print("Client Response:", data)
        
        # Verify success
        if "secret data" in str(data):
            print("SUCCESS: Retrieved secret data!")
            return True
        else:
            print("FAILURE: Did not find secret data.")
            return False

    finally:
        # Cleanup
        print("Stopping servers...")
        auth_proc.terminate()
        client_proc.terminate()
        resource_proc.terminate()
        
        # Wait a bit to ensure ports are freed
        time.sleep(1)

if __name__ == "__main__":
    success = test_flow()
    if not success:
        sys.exit(1)
