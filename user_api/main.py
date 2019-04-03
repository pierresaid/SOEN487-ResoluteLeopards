import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from jwcrypto import jwt, jws, jwk
from exceptions import ApiError
from config import DevConfig
from keys import load_keys, load_key

app = Flask(__name__)
CORS(app)

app.config.from_object(DevConfig)

# Signing Keys have to be loaded on start
keys = load_keys(os.path.join(os.path.dirname(__file__), app.config["KEY_LIST_PATH"]))
key = load_key(keys)

from views import user, auth

app.register_blueprint(user.bp)
app.register_blueprint(auth.bp)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/jwt/key')
def obtain_public_key():
    r = app.make_response(keys.export(private_keys=False))
    r.headers["Content-Type"] = "application/json"
    return r


@app.route('/jwt/obtain')
def obtain_token():
    token = jwt.JWT(header={"alg": "RS256"}, claims={"info": "I'm a signed token"})
    token.make_signed_token(key)
    return jsonify({"token": token.serialize()})


@app.route('/jwt/verify')
def verify_token():
    authorization = request.headers.get("Authorization")
    [type, token] = authorization.split(" ")
    print("token: ", token)
    public_key = jwk.JWK.from_json(key.export_public())
    try:
        tok = jwt.JWT(jwt=token).token
        tok.verify(public_key)
        return jsonify({"valid": True})
    except jws.InvalidJWSSignature:
        return jsonify({"valid": False})
    except:
        raise ApiError(400, "Invalid token format")


if __name__ == '__main__':
    app.run()
