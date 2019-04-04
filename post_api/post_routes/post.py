from flask import Blueprint, request, jsonify, make_response
from post_models import Post
from main import db, app
from sqlalchemy import exc
from utils import row2dict

post_blueprint = Blueprint('post', __name__)


@app.route('/post', methods={'GET'})
def get_all_post():
    page_size = request.args.get('post_per_page')
    page = request.args.get('page')
    posts = Post.query.order_by(Post.id)
    for post in posts:
        print(post)
    if page is None or page_size is None:
        return jsonify({'code': 200, 'posts': [row2dict(p) for p in posts]})

    try:
        posts = [posts[i: i + int(page_size)] for i in range(0, posts.count(), int(page_size))][int(page)]
        return jsonify({'code': 200, 'posts': [row2dict(i) for i in posts]})
    except IndexError:
        return jsonify({'code': 200, 'end' : True, 'posts': [row2dict(i) for i in posts]})


@app.route('/post/<post_id>', methods={'GET'})
def get_post_by_id(post_id: int):
    post = Post.query.filter_by(id=post_id)
    if post:
        return jsonify({'code': 200, 'post': post})
    else:
        return jsonify({'code': 404, 'error': f'Post with id {post_id}, cannot be found'})


@app.route('/post', methods={'POST'})
def put_new_post():
    data = request.get_json()

    try:
        params = {
            'author_id': data['user_id'],
            'url_one': data['url_one'],
            'url_two': data['url_two'],
            'title': data['title']
        }
    except:
        return make_response(jsonify({'code': 400, 'error': 'Badly formed request, parameters are missing'}))

    p = Post(**params)
    db.session.add(p)
    try:
        db.session.commit()
    except exc.IntegrityError:
        error = 'wrong parameters sent\n'
        return make_response(jsonify({"code": 400, "error": error}), 400)
    return make_response(jsonify({"code": 200, "post": row2dict(p)}), 200)

