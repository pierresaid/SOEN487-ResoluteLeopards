import sqlalchemy
from flask import Blueprint, make_response, request
from flask import jsonify
from werkzeug.exceptions import BadRequestKeyError

from utils import row2dict
from main import app, db
from post_models import Vote

vote_blueprint = Blueprint('vote', __name__, url_prefix='/vote')

#region GET
@vote_blueprint.route("", methods={'GET'})
def get_all_votes():
    vote_list = Vote.query.all()
    return jsonify([row2dict(vote) for vote in vote_list])


@vote_blueprint.route("/<post_id>/<user_id>", methods={'GET'})
def get_vote(post_id, user_id):
    vote = Vote.query.filter_by(post_id=post_id, user_id=user_id).first()
    if vote:
        return jsonify(row2dict(vote))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this vote."}), 404)


@vote_blueprint.route("/<post_id>", methods={'GET'})
def get_vote_for_post(post_id):
    vote_list = Vote.query.filter_by(post_id=post_id)
    if vote_list:
        return jsonify([row2dict(vote) for vote in vote_list])
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this post's votes."}), 404)


@vote_blueprint.route("/user/<user_id>", methods={'GET'})
def get_vote_for_user(user_id):
    vote_list = Vote.query.filter_by(user_id=user_id)
    if vote_list:
        return jsonify([row2dict(vote) for vote in vote_list])
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this user's votes."}), 404)
#endregion
#region PUT/POST
# TODO: Revove userId when we'll have the token
@vote_blueprint.route("/<post_id>/<user_id>", methods={'PUT'})
def update_vote(post_id, user_id):
    vote = Vote.query.filter_by(post_id=post_id, user_id=user_id).first()
    if vote:
        if 'value' in request.form:
            vote.value = request.form['value']
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot update vote.\n"
            print(app.config.get("DEBUG"))
            if app.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 400, "msg": error}), 404)
        return jsonify(row2dict(vote))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this vote."}), 404)


@vote_blueprint.route("/", methods={'POST'})
def add_vote():
    try:
        data = request.form
        param = {
            'post_id': data['post_id'],
            'user_id': data['user_id'],
            'value': data['value']
        }
    except BadRequestKeyError:
        return make_response(jsonify({"code": 400, "msg": "Request is missing fields"}), 400)

    new_vote = Vote(**param)
    db.session.add(new_vote)

    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        return make_response(jsonify({"code": 404, "msg": e}), 404)
    return jsonify(row2dict(new_vote))
#endregion
#region DELETE
@vote_blueprint.route("/<post_id>/<user_id>", methods=['DELETE'])
def delete_vote(post_id, user_id):
    vote = Vote.query.filter_by(post_id=post_id, user_id=user_id).first()
    if vote:
        db.session.delete(vote)
        db.session.commit()
        return jsonify({"code": 200, "msg": "success"})
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this vote."}), 404)
#endregion
