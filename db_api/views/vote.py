import sqlalchemy
from flask import Blueprint, make_response, request
from flask import jsonify
from werkzeug.exceptions import BadRequestKeyError

from main import app
from models import Vote, row2dict, db

bp = Blueprint('vote', __name__, url_prefix='/vote')


@bp.route("/")
def get_all_votes():
    vote_list = Vote.query.all()
    return jsonify([row2dict(vote) for vote in vote_list])


@bp.route("/<post_id>/<user_id>")
def get_vote(post_id, user_id):
    vote = Vote.query.filter_by(post_id=post_id, user_id=user_id).first()
    if vote:
        return jsonify(row2dict(vote))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this vote."}), 404)


@bp.route("/<post_id>")
def get_vote_for_post(post_id):
    vote_list = Vote.query.filter_by(post_id=post_id)
    if vote_list:
        return jsonify([row2dict(vote) for vote in vote_list])
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this post's votes."}), 404)


@bp.route("/user/<user_id>")
def get_vote_for_user(user_id):
    vote_list = Vote.query.filter_by(user_id=user_id)
    if vote_list:
        return jsonify([row2dict(vote) for vote in vote_list])
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this user's votes."}), 404)


@bp.route("/<post_id>/<user_id>", methods=['PUT'])
def update_vote(post_id, user_id):
    vote = Vote.query.filter_by(post_id=post_id, user_id=user_id).first()
    if vote:
        if 'value' in request.form:
            vote.value = request.form['value']
        try:
            db.session.commit()
            updated_vote = Vote.query.filter_by(post_id=post_id, user_id=user_id).first()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot update vote. "
            print(app.config.get("DEBUG"))
            if app.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 404, "msg": error}), 404)
        return jsonify(row2dict(updated_vote))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this vote."}), 404)


@bp.route("/", methods=['POST'])
def add_vote():
    try:
        newVote = Vote(post_id=request.form['post_id'], user_id=request.form['user_id'], value=request.form['value'])
    except BadRequestKeyError:
        return make_response(jsonify({"code": 400, "msg": "missing fields"}), 400)
    db.session.add(newVote)
    try:
        db.session.commit()
        added_vote = Vote.query.filter_by(user_id=newVote.user_id, post_id=newVote.post_id).first()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot add vote."
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify(row2dict(added_vote))


@bp.route("/<post_id>/<user_id>", methods=['DELETE'])
def delete_vote(post_id, user_id):
    vote = Vote.query.filter_by(post_id=post_id, user_id=user_id).first()
    if vote:
        db.session.delete(vote)
        db.session.commit()
        return jsonify({"code": 200, "msg": "success"})
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this vote."}), 404)
