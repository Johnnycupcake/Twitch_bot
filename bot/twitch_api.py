import os
import requests
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')
BASE_URL =  'https://api.twitch.tv/helix/'

def get_access_token():
    #Figure out flow and figure out scopes
    
    url = 'https://id.twitch.tv/oauth2/token'
    parameters = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=parameters)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get access token: {response.status_code} {response.text}")
    
def get_user_id(access_token):
    url = f"{BASE_URL}users"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-ID': CLIENT_ID
    }
    params = {
        'login': CHANNEL_NAME
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['data'][0]['id']
        
    else:
        raise Exception(f"Failed to get user ID: {response.status_code} {response.text}")
    
def get_stream_info(access_token, user_id):
    url = f"{BASE_URL}streams"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-ID': CLIENT_ID
    }
    params = {
        'user_id': user_id
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print(response)
        if response.json()['data'] == []:
            return f"{CHANNEL_NAME} is offline"
        else:
             return response.json()['data']
    elif response.status_code == 204:
        return "Stream is offline"
    else:
        raise Exception(f"Failed to get stream info: {response.status_code} {response.text}")
    
def get_followers(access_token, user_id):
    url = f"{BASE_URL}users/follows"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-ID': CLIENT_ID
    }
    params = {
        'to_id': user_id,
        'first': 100
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['total']
    else:
        raise Exception(f"Failed to get followers: {response.status_code} {response.text}")
    
    