from flask import Blueprint, request
from flask import jsonify
from argon2 import PasswordHasher

from exceptions import ApiError
from helpers.user import get_user_by_email, create_new_user
from helpers.jwt import create_tokens_for_user, get_fresh_token

bp = Blueprint('auth', __name__, url_prefix='/auth')
ph = PasswordHasher()

@bp.route("/login", methods=['POST'])
def login():
    # Validate request form
    mail = request.form['mail']
    password = request.form['password']
    if not mail and not password:
        return jsonify({"code": 400, "msg": "Bad Request"}), 400

    # Compare credentials
    user = get_user_by_email(mail)
    if not user:
        return jsonify({"code": 401, "msg": "Unauthorized: wrong email or password"}), 401
    try:
        ph.verify(user.pwdhash, password)
    except:
        print(f"Couldn't verify '{user.pwdhash}' and '{password}' w/ Argon2id.")
        return jsonify({"code": 401, "msg": "Unauthorized: wrong email or password"}), 401

    # Successful: Create the token
    tokens = create_tokens_for_user(user)

    # Send token to the user
    return jsonify({"code": 200, "msg": "Success", **tokens}), 200


@bp.route("/register", methods=['POST'])
def register():
    try:
        # Create the new user
        user = create_new_user(request.form.get("name"), request.form.get("mail"), request.form.get("password"))
    except ApiError as e:
        return jsonify({"code": e.code, "msg": e.msg}), e.code

    tokens = create_tokens_for_user(user)

    # Send token to the user
    return jsonify({"code": 200, "msg": "Success", **tokens}), 200


@bp.route("/token/<refresh_token>", methods=['GET'])
def refresh(refresh_token):
    try:
        token = get_fresh_token(refresh_token)
    except ApiError as e:
        return jsonify({"code": e.code, "msg": e.msg}), e.code

    # Send fresh token to the user
    return jsonify({"code": 200, "msg": "Success", "access_token": token}), 200
