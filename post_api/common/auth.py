import requests
from functools import wraps
from flask import g, request, redirect, url_for
from jwcrypto import jwk, jwt, jws
from jwcrypto.common import json_decode
from datetime import datetime
import pytz

token_blacklist = set()


def get_token_blacklist():
    pass


def init_token_blacklist():
    pass


def setup_auth(auth_api_url: str):
    """
    :param auth_api_url: base url of the authorization service (API)

    Function to be called once at the start of a service.

    Obtains the public keys of the Authorization service in order to verify JWT tokens.
    """
    r = requests.get(auth_api_url + "/jwt/key")
    if r.status_code == 200 and r.headers['content-type'] == 'application/json':
        global public_keys
        public_keys = jwk.JWKSet.from_json(r.content)
        print("[Auth] Using Public Keys: ", public_keys.export())
    else:
        print("request failed status: ", r.status_code, r.headers['content-type'])
    pass


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Get authorization header
        authorization = request.headers.get("Authorization")
        if not authorization:
            return "No authorization header", 400

        # Get token from HTTP Authorization Header
        [type, token] = authorization.split(" ")
        if not (type or token):
            return "Incorrect authorization header", 400

        try:
            # Obtain / verify token
            tok: jws.JWS = jwt.JWT(jwt=token).token
            tok.verify(public_keys)
            payload = json_decode(tok.payload)

            # Check if the token is expired
            exp = datetime.utcfromtimestamp(payload['exp']).replace(tzinfo=pytz.utc)
            if exp < datetime.now(tz=pytz.utc):
                return f"Token expired {abs(int((exp - datetime.now(tz=pytz.utc)).total_seconds()))} seconds ago", 401

            # Set the user id
            g.user_id = payload['user_id']

            # Pass on the request
            return f(*args, **kwargs)
        except jws.InvalidJWSSignature:
            return "Unable to verify signature", 401
        except:
            return "Invalid token", 401

    return wrapper
