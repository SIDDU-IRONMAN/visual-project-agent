import os
import sys
import urllib.request
import json
from dotenv import load_dotenv

def check_env():
    print("Checking .env file...")
    load_dotenv()
    required_keys = ["GEMINI_API_KEY", "FIRECRAWL_API_KEY"]
    missing = [key for key in required_keys if not os.getenv(key)]
    
    if missing:
        print(f"FAILED: Missing environment variables: {', '.join(missing)}")
        return False
    print("SUCCESS: Environment variables are set.")
    return True

def check_backend():
    print("Checking Backend connectivity (http://localhost:8000/health)...")
    try:
        with urllib.request.urlopen("http://localhost:8000/health", timeout=5) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode())
                if data.get("status") == "ok":
                    print("SUCCESS: Backend is reachable and healthy.")
                    return True
    except Exception as e:
        print(f"FAILED: Could not reach backend: {e}")
    return False

def check_frontend():
    print("Checking Frontend connectivity (http://localhost:5500)...")
    try:
        with urllib.request.urlopen("http://localhost:5500", timeout=5) as response:
            if response.getcode() == 200:
                print("SUCCESS: Frontend is reachable.")
                return True
    except Exception as e:
        print(f"FAILED: Could not reach frontend: {e}")
    return False

if __name__ == "__main__":
    env_ok = check_env()
    print("-" * 30)
    # Backend/Frontend checks are only useful if they are already running
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    
    if env_ok and backend_ok and frontend_ok:
        print("\nOVERALL STATUS: ALL SYSTEMS GO!")
        sys.exit(0)
    else:
        print("\nOVERALL STATUS: SOME CHECKS FAILED.")
        print("Note: Backend and Frontend checks require the servers to be running.")
        sys.exit(1)
