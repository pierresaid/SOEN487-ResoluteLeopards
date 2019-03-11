import sqlalchemy
from models import User, db
from werkzeug.exceptions import BadRequestKeyError
from exceptions import ApiError


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_user_by_email(user_mail):
    return User.query.filter_by(mail=user_mail).first()


def create_new_user(name, mail, pwdhash):
    try:
        new_user = User(name=name, mail=mail, pwdhash=pwdhash)
    except BadRequestKeyError:
        raise ApiError(400, "missing parameters")
    db.session.add(new_user)
    try:
        db.session.commit()
        # added_user = User.query.filter_by(id=new_user.id).first()
    except sqlalchemy.exc.SQLAlchemyError as e:
        raise ApiError(500, "unable to persist user")
    return new_user
