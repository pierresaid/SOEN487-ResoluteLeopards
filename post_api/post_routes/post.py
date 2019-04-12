from flask import Blueprint, request, jsonify, make_response
from post_models import Post, Vote
from main import db, app
from common.auth import login_required
from sqlalchemy import exc, desc
from utils import row2dict

post_blueprint = Blueprint('post', __name__)

# TODO: Get the user name from the user table.
@post_blueprint.route('/post', methods={'GET'})
def get_all_post():
    page_size = convert_value_or_none(request.args.get('post_per_page'))
    page = convert_value_or_none(request.args.get('page'))
    user_id = convert_value_or_none(request.args.get('user_id'))
    
    full_json_posts = [row2dict(p) for p in Post.query.order_by(desc(Post.id))]
    if page is None or page_size is None:
        add_votes_to_post_json_list(full_json_posts, user_id)
        return jsonify({'code': 200, 'posts': full_json_posts})
    try:
        """
            In this line we do the pagination. 
            range(0, posts.count() will produce a list from 0 to posts.count() by increment of page_size.
            We then use those numbers to select the page of posts we want
        """
        posts = [full_json_posts[i: i + page_size] for i in range(0, len(full_json_posts), page_size)]
        posts = posts[page]
        add_votes_to_post_json_list(posts, user_id)
        return jsonify({'code': 200, 'posts': posts})
    except IndexError:
        return jsonify({'code': 200, 'end': True})


def convert_value_or_none(value) -> int or None:
    try:
        return int(value)
    except TypeError:
        return None


def add_votes_to_post_json_list(post_list: list, user_id: int):
    for post in post_list:
        vote = Vote.query.filter_by(post_id=post['id'], user_id=user_id)
        if user_id:
            user_vote = [x for x in vote if x.user_id == user_id]
            post['user_vote'] = int(-1 if not user_vote else user_vote[0].value)
        post['vote_one'] = int(sum(v.value == 0 for v in vote))
        post['vote_two'] = int(sum(v.value == 1 for v in vote))


@post_blueprint.route('/post/<post_id>', methods={'GET'})
def get_post_by_id(post_id: int):
    post = Post.query.filter_by(id=post_id).first()
    
    json_post = row2dict(post)
    user_id = convert_value_or_none(request.args.get('user_id'))
    if user_id is not None:
        add_votes_to_post_json_list([json_post], user_id)
    
    if post:
        return jsonify({'code': 200, 'post': json_post})
    else:
        return make_response(jsonify({'code': 404, 'msg': 'Cannot find this post.'}), 404)

@post_blueprint.route('/post/<post_id>', methods={'DELETE'})
@login_required
def delete_post_by_post_id(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'code': 200, 'msg': 'success'})
    else:
        return make_response(jsonify({'code': 404, 'msg': 'Cannot find this post.'}), 404)


@post_blueprint.route('/post', methods={'POST'})
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
        return make_response(jsonify({'code': 400, 'msg': 'Badly formed request, parameters are missing'}), 400)

    p = Post(**params)
    db.session.add(p)
    try:
        db.session.commit()
    except exc.IntegrityError:
        error = 'wrong parameters sent\n'
        return make_response(jsonify({"code": 400, "error": error}), 400)
    return make_response(jsonify({"code": 200, "post": row2dict(p)}), 200)


