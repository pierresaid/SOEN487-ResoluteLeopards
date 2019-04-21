import os
from datetime import timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from jwcrypto import jwt, jws, jwk
from exceptions import ApiError
from config import DevConfig, ProdConfig
from keys import load_keys, get_keys, get_signing_key
from helpers.jwt_claims import jwt_claims

app = Flask(__name__)
CORS(app)

if not app.config['TESTING']:
    if os.environ.get('PRODUCTION'):
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)

# Signing Keys have to be loaded on start
load_keys(app.config["KEY_LIST_PATH"])

from views import user, auth

app.register_blueprint(user.bp)
app.register_blueprint(auth.bp)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/jwt/key')
def obtain_public_key():
    r = app.make_response(get_keys().export(private_keys=False))
    r.headers["Content-Type"] = "application/json"
    return r


@app.route('/jwt/obtain')
def obtain_token():
    token = jwt.JWT(header={"alg": "RS256", "typ": "JWT"}, claims=jwt_claims(timedelta(hours=24), **{"info": "I'm a signed token"}))
    token.make_signed_token(get_signing_key())
    return jsonify({"token": token.serialize()})


def key_set_verify(token, key_set):
    for key in key_set.__iter__():
        try:
            token.verify(key)
            return key
        except jws.InvalidJWSSignature:
            pass
    raise Exception("Unable to verify signature")


@app.route('/jwt/verify')
def verify_token():
    authorization = request.headers.get("Authorization")
    [type, token] = authorization.split(" ")
    try:
        tok = jwt.JWT(jwt=token).token
        key_set_verify(tok, jwk.JWKSet.from_json(get_keys().export(private_keys=False)))
        return jsonify({"valid": True})
    except jws.InvalidJWSSignature:
        return jsonify({"valid": False})
    except:
        raise ApiError(400, "Invalid token format")


@app.errorhandler(404)
def not_found(e):
    return jsonify({"code": 404, "msg": "Not Found"}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"code": 500, "msg": "Internal Server Error"}), 500


if __name__ == '__main__':
    app.run()
