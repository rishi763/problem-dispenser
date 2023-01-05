import bcrypt
import os
import requests


def get_discord_auth_url():
    return "https://discord.com/api/oauth2/authorize?client_id={}&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Flogin&response_type=code&scope=identify".format(os.environ["CLIENT_ID"])


def get_user_tokens(code):
    data={
        'client_id':os.environ["CLIENT_ID"],
        'client_secret':os.environ["CLIENT_SECRET"],
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.environ["REDIRECT_URI"]
    }
    headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    request=requests.post("https://discord.com/api/v9/oauth2/token" ,data=data, headers=headers)
    if 'access_token' not in request.json():
        return None
    else:
        return request.json()


def update_user_tokens(refresh_code):
    data={
        'client_id':os.environ["CLIENT_ID"],
        'client_secret':os.environ["CLIENT_SECRET"],
        'grant_type': 'refresh_token',
        'refresh_token': refresh_code,
    }
    headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    request=requests.post("https://discord.com/api/v9/oauth2/token" ,data=data, headers=headers)
    if 'access_token' not in request.json():
        return None
    else:
        return request.json()


def get_user_info(token):
    headers={
        "Authorization": "Bearer "+str(token)
    }
    request=requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    if request.status_code==401:
        return None
    return request.json()


def create_cookie_hash(id):
    salt=bcrypt.gensalt()
    hash=bcrypt.hashpw(bytes(id, 'utf-8'), salt)
    return (str(hash), str(salt))