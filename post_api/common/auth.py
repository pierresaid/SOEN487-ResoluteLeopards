import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from functools import wraps
from flask import g, request, jsonify
from jwcrypto import jwk, jwt, jws
from jwcrypto.common import json_decode
from datetime import datetime
from common.exceptions import ApiError, TokenVerificationException


Retry.BACKOFF_MAX = 5


def requests_retry_session(
    retries=100,
    backoff_factor=0.1,
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(500,)
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def setup_auth(auth_api_url: str):
    """
    :param auth_api_url: base url of the authorization service (API)

    Function to be called once at the start of a service.

    Obtains the public keys of the Authorization service in order to verify JWT tokens.
    """
    t0 = datetime.now()
    print(f"Trying to obtaining public keys from '{auth_api_url}', waiting...")
    try:
        r = requests_retry_session().get(auth_api_url + "/jwt/key")
    except Exception:
        raise Exception(f"Failed to obtain public keys after trying for {(datetime.now() - t0).total_seconds()}s")
    else:
        if r.status_code == 200 and r.headers['content-type'] == 'application/json':
            global public_keys
            public_keys = jwk.JWKSet.from_json(r.content)
            print("[Auth] Using Public Keys: ", public_keys.export())
        else:
            raise Exception(f"Failed to obtain public keys status: {r.status_code}")
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
