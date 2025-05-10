import os
import requests
import urllib.parse
from dotenv import load_dotenv
from bot.json_loader import save_tokens, load_tokens

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
BASE_URL = 'https://api.twitch.tv/helix/'




def gen_auth_url():
    url = 'https://id.twitch.tv/oauth2/authorize'
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'user:read:email user:edit user:manage:blocked_users user:read:blocked_users'
    }
    auth_url = f"{url}?{urllib.parse.urlencode(params)}"
    print("Visit this URL to authorize the app:")
    print(auth_url)


def exchange_for_tokens(code):
    url = 'https://id.twitch.tv/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        save_tokens(tokens)
        return tokens['access_token']
    else:
        raise Exception(f"Error exchanging code for tokens: {response.status_code} - {response.text}")


def refresh_access_token(refresh_token):
    url = 'https://id.twitch.tv/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        save_tokens(tokens)
        return tokens['access_token']
    else:
        raise Exception(f"Error refreshing access token: {response.status_code} - {response.text}")


def get_user_info():
    tokens = load_tokens()
    if not tokens:
        print("❗ No tokens found. Run gen_auth_url(), go to the URL, get the code, and call exchange_for_tokens(code).")
        return

    access_token = tokens['access_token']

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-ID': CLIENT_ID
    }
    url = f"{BASE_URL}users"
    response = requests.get(url, headers=headers)

    # Handle token expiration
    if response.status_code == 401:
        print("🔁 Access token expired. Refreshing...")
        access_token = refresh_access_token(tokens['refresh_token'])

        headers['Authorization'] = f'Bearer {access_token}'
        response = requests.get(url, headers=headers)

    print(response.status_code, response.json())
    return response.json()

