import requests
from functools import wraps
from flask import g, request, redirect, url_for
from jwcrypto import jwk, jwt, jws
from jwcrypto.common import json_decode
from datetime import datetime
import pytz

token_blacklist = set()

def get_jwt_public_signing_key(auth_api_url: str):
    pass


def get_token_blacklist():
    pass


def init_token_blacklist():
    pass


def setup_auth(auth_api_url: str):
    r = requests.get(auth_api_url + "/jwt/key")
    if r.status_code == 200 and r.headers['content-type'] == 'application/json':
        global public_key
        public_key = jwk.JWK.from_json(r.content)
        print("[Auth] Using Public Key: ", public_key.export())
    else:
        print("request failed status: ", r.status_code, r.headers['content-type'])
    pass


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        authorization = request.headers.get("Authorization")
        if not authorization:
            return "No authorization header", 400

        [type, token] = authorization.split(" ")
        if not (type or token):
            return "Incorrect authorization header", 400

        try:
            tok: jws.JWS = jwt.JWT(jwt=token).token
            tok.verify(public_key)
            payload = json_decode(tok.payload)
            exp = datetime.utcfromtimestamp(payload['exp']).replace(tzinfo=pytz.utc)
            if exp < datetime.now(tz=pytz.utc):
                return f"Token expired {abs(int((exp - datetime.now(tz=pytz.utc)).total_seconds()))} seconds ago", 401
            g.user_id = payload['user_id']
            return f(*args, **kwargs)
        except jws.InvalidJWSSignature:
            return "Unable to verify signature", 401
        except:
            return "Invalid token", 401
        # return f(*args, **kwargs)
    return wrapper
