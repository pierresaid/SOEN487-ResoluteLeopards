from flask import Flask, request, jsonify
from jwcrypto import jwt, jws, jwk
from config import DevConfig
import json
import os

app = Flask(__name__)
app.config.from_object(DevConfig)

key = None
# TODO: read key location from config + add *.pem to gitignore
with open(os.path.dirname(os.path.realpath(__file__)) + "/key.pem", mode="rb") as f:
    # keys = [jwk.construct(key) for key in json.loads(f.read())["keys"]]
    # keys = jwk.JWKSet.from_json(f.read())
    key = jwk.JWK.from_pem(f.read(), b"123456") # jwk.JWK.from_json(f.read())
    print(key)

from views import user, auth

app.register_blueprint(user.bp)
app.register_blueprint(auth.bp)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/jwt/key')
def obtain_public_key():
    r = app.make_response(key.export_public())
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/jwt/obtain')
def obtain_token():
    token = jwt.JWT(header={"alg": "RS256"}, claims={"info": "I'm a signed token"})
    #key = keys.get_key("001")
    print(key.export())
    token.make_signed_token(key)
    return token.serialize()

@app.route('/jwt/verify')
def verify_token():
    authorization = request.headers.get("Authorization")
    [type, token] = authorization.split(" ")
    print("token: ", token)
    public_key = jwk.JWK.from_json(key.export_public())
    try:
        tok = jwt.JWT(jwt=token).token
        tok.verify(public_key)
        return "Valid token"
    except jws.InvalidJWSSignature:
        return "Unable to verify signature"
    except:
        return "Invalid token"


if __name__ == '__main__':
    app.run()
