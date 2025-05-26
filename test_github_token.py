import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the token from .env
token = os.getenv("GITHUB_TOKEN")

if not token:
    print("❌ GITHUB_TOKEN is missing or not loaded.")
    exit()

# Make a test API request
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

response = requests.get("https://api.github.com/user", headers=headers)

if response.status_code == 200:
    print("✅ Token is working! GitHub username:", response.json().get("login"))
else:
    print("❌ Token test failed. Status code:", response.status_code)
    print(response.json())
