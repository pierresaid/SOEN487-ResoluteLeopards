import requests
from functools import wraps
from flask import g, request, jsonify
from jwcrypto import jwk, jwt, jws
from jwcrypto.common import json_decode
from common.exceptions import ApiError, TokenVerificationException


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


def key_set_verify(token, key_set):
    for key in key_set.__iter__():
        try:
            token.verify(key)
            return key
        except jws.InvalidJWSSignature:
            pass
    raise TokenVerificationException("Unable to verify signature")


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            # Get authorization header
            authorization = request.headers.get("Authorization")
            if not authorization:
                raise ApiError(400, "No authorization header")

            # Get token from HTTP Authorization Header
            [type, token] = authorization.split(" ")
            if not (type or token):
                raise ApiError(400, "Incorrect authorization header")

            try:
                # Obtain / verify token
                tok: jws.JWS = jwt.JWT(jwt=token).token
                key_set_verify(tok, public_keys)
                payload = json_decode(tok.payload)

                # Set the user id
                if 'user_id' not in payload:
                    raise ApiError(400, "No user_id contained in the token")
                g.user_id = payload['user_id']

                # Pass on the request
                return f(*args, **kwargs)
            except TokenVerificationException:
                raise ApiError(401, "Unable to verify signature")
            except jwt.JWTExpired:
                raise ApiError(401, "Token has expired")
            except jwt.JWException:
                raise ApiError(401, "Invalid token")
        except ApiError as e:
            return jsonify({"code": e.code, "msg": e.msg}), e.code

    return wrapper
