import os
import sqlalchemy
from models import User, db
from werkzeug.exceptions import BadRequestKeyError
from exceptions import ApiError
from argon2 import PasswordHasher

ph = PasswordHasher()


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_user_by_email(user_mail):
    return User.query.filter_by(mail=user_mail).first()


def hash_password(password: str):
    return ph.hash(password)


def create_new_user(name, mail, password):
    try:
        new_user = User(name=name, mail=mail, pwdhash=hash_password(password))
    except BadRequestKeyError:
        raise ApiError(400, "missing parameters")
    db.session.add(new_user)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        raise ApiError(500, "unable to persist user")
    return new_user
