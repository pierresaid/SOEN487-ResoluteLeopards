import sqlalchemy
from flask import Blueprint, make_response, request
from flask import jsonify
from werkzeug.exceptions import BadRequestKeyError

from main import app
from models import Post, row2dict, db

bp = Blueprint('post', __name__, url_prefix='/post')


@bp.route("/")
def get_all_posts():
    post_list = Post.query.all()
    return jsonify([row2dict(post) for post in post_list])


@bp.route("/<post_id>")
def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        return jsonify(row2dict(post))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this post."}), 404)


@bp.route("/<post_id>", methods=['PUT'])
def update_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        if 'title' in request.form:
            post.title = request.form['title']
        if 'url_one' in request.form:
            post.url_one = request.form['url_one']
        if 'url_two' in request.form:
            post.url_two = request.form['url_two']
        try:
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error = "Cannot update post. "
            print(app.config.get("DEBUG"))
            if app.config.get("DEBUG"):
                error += str(e)
            return make_response(jsonify({"code": 404, "msg": error}), 404)
        return jsonify({"code": 200, "msg": "success"})
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this post."}), 404)


@bp.route("/", methods=['POST'])
def add_post():
    try:
        newPost = Post(title=request.form['title'], url_one=request.form['url_one'], url_two=request.form['url_two'])
    except BadRequestKeyError:
        return make_response(jsonify({"code": 400, "msg": "missing parameters"}), 400)
    db.session.add(newPost)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot add post."
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})


@bp.route("/<post_id>", methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        try:
            db.session.delete(post)
            db.session.commit()
            return jsonify({"code": 200, "msg": "success"})
        except sqlalchemy.exc.IntegrityError:
            return make_response(jsonify({"code": 400, "msg": "This post has existing vote"}), 400)
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this post."}), 404)
