from datetime import datetime, timedelta

import jwt
from django.conf.global_settings import SECRET_KEY

from app.exceptions.exceptions import Unauthorized
from uniflow.settings import JWT_ACCESS_TOKEN_EXPIRATION_TIME, JWT_REFRESH_TOKEN_EXPIRATION_TIME


def generate_tokens(payload):
    refresh_token = generate_refresh_token(payload)
    access_token = generate_access_token(payload)
    return access_token, refresh_token


def generate_access_token_from_refresh(refresh_token):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])
        if 'exp' in payload and datetime.utcfromtimestamp(payload['exp']) > datetime.utcnow():
            new_payload = {'user_id': payload['user_id']}
            return generate_access_token(new_payload)
    except jwt.ExpiredSignatureError:
        raise Unauthorized("Access Token Expired")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid Token")


def generate_refresh_token(payload):
    expiration_time = datetime.now() + timedelta(minutes=JWT_REFRESH_TOKEN_EXPIRATION_TIME)
    payload['exp'] = expiration_time
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def generate_access_token(payload):
    expiration_time = datetime.now() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRATION_TIME)
    payload['exp'] = expiration_time
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithm='HS256')
    except jwt.ExpiredSignatureError:
        raise Unauthorized("Access Token Expired")
    except jwt.DecodeError:
        raise Unauthorized("Invalid Token")
