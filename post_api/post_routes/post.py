from flask import Blueprint, request, jsonify, make_response
from post_models import Post
from main import db, app
from sqlalchemy import exc
from utils import row2dict

post_blueprint = Blueprint('post', __name__)


@app.route('/post/', methods={'GET'})
def get_all_post():
    posts = Post.query.order_by(Post.id)
    for post in posts:
        print(post)
    return jsonify({'code': 200, 'posts': [row2dict(p) for p in posts]})


@app.route('/post/<post_id>', methods={'GET'})
def get_post_by_id(post_id: int):
    post = Post.query.filter_by(id=post_id)
    if post:
        return jsonify({'code': 200, 'post': post})
    else:
        return jsonify({'code': 404, 'error': f'Post with id {post_id}, cannot be found'})


@app.route('/post', methods={'PUT'})
def put_new_post():
    params = {
        'url_one': request.form.get('cat'),
        'url_two': request.form.get('dog'),
        'title': request.form.get('title')
    }

    p = Post(**params)
    db.session.add(p)
    try:
        db.session.commit()
    except exc.IntegrityError as e:
        error = 'wrong parameters sent\n'
        return make_response(jsonify({"code": 400, "error": error}), 400)
    return make_response(jsonify({"code": 200, "msg": f"{p}"}), 200)

