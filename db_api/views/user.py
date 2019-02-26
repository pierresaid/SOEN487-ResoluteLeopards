import sqlalchemy
from flask import Blueprint, make_response, request
from flask import jsonify
from werkzeug.exceptions import BadRequestKeyError

from main import app
from models import User, row2dict, db

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route("/")
def get_all_users():
    user_list = User.query.all()
    return jsonify([row2dict(user) for user in user_list])


@bp.route("/<user_id>")
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify(row2dict(user))
    else:
        return make_response(jsonify({"code": 404, "msg": "User not found"}), 404)


@bp.route("/<user_id>", methods=['PUT'])
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        if 'name' in request.form:
            user.name = request.form['name']
        try:
            db.session.commit()
            updated_user = User.query.filter_by(id=user_id).first()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot update user. "
            print(app.config.get("DEBUG"))
            if app.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 404, "msg": error}), 404)
        return jsonify(row2dict(updated_user))
    else:
        return make_response(jsonify({"code": 404, "msg": "User not found"}), 404)


@bp.route("/", methods=['POST'])
def add_user():
    try:
        newUser = User(name=request.form['name'])
    except BadRequestKeyError:
        return make_response(jsonify({"code": 400, "msg": "missing name"}), 400)
    db.session.add(newUser)
    try:
        db.session.commit()
        added_user = User.query.filter_by(id=newUser.id).first()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot add user."
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify(row2dict(added_user))


@bp.route("/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"code": 200, "msg": "success"})
        except sqlalchemy.exc.IntegrityError:
            return make_response(jsonify({"code": 400, "msg": "This user has existing votes"}), 400)
    else:
        return make_response(jsonify({"code": 404, "msg": "User not found"}), 404)
