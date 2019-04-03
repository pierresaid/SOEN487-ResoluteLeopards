import sqlalchemy
from flask import Blueprint, request, jsonify, g
from exceptions import ApiError
from werkzeug.exceptions import BadRequestKeyError
from decorators import accept_fields, require_fields, hash_password_field

from models import User, db
from helpers.user import create_new_user, hash_password

bp = Blueprint('user', __name__, url_prefix='/users')


def filter_empty(d: dict):
    return {k: v for k, v in d.items() if v is not None}


@bp.route("/")
def get_users():
    # Obtain supported args to filter users by
    args = filter_empty({
        "name": request.args.get("name", None)
    })

    # Get the list
    user_list = User.query.filter_by(**args)
    user_list = [user.export_public() for user in user_list]
    return jsonify(user_list)


@bp.route("/<int:user_id>")
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify(user.export_public())
    else:
        return jsonify({"code": 404, "msg": "User not found"}), 404


@bp.route("/<string:user_mail>")
def get_user_complete(user_mail):
    user = User.query.filter_by(mail=user_mail).first()
    if user:
        return jsonify(user.export_public())
    else:
        return jsonify({"code": 404, "msg": "User not found"}), 404


@bp.route("/<user_id>", methods=['PUT'])
@accept_fields("name", "mail", "password")
@hash_password_field
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        # Update existing user
        try:
            user.update(g.data)
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return jsonify({"code": 404, "msg": "Unable to update the user"}), 404
        return jsonify(user.export_public())
    else:
        # Create new user at id
        try:
            user = User(id=user_id, **g.data)
            db.session.add(user)
            db.session.commit()
        except BadRequestKeyError:
            raise ApiError(400, "missing parameters")
        except sqlalchemy.exc.SQLAlchemyError as e:
            return jsonify({"code": 500, "msg": "unable to persist user"}), 500
    return jsonify(user.export_public())


@bp.route("/", methods=['POST'])
@require_fields("name", "mail", "password")
def add_user():
    try:
        added_user = create_new_user(**g.data)
    except ApiError as e:
        return jsonify({"code": e.code, "msg": e.msg}), e.code
    return jsonify(added_user.export_public())


@bp.route("/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"code": 200, "msg": "success"})
        except sqlalchemy.exc.IntegrityError:
            return jsonify({"code": 400, "msg": "Unable to delete this user"}), 400
    else:
        return jsonify({"code": 404, "msg": "User not found"}), 404
