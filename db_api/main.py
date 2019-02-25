from flask import Flask, jsonify, make_response

from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)

from views import user, post, vote

app.register_blueprint(user.bp)
app.register_blueprint(post.bp)
app.register_blueprint(vote.bp)


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route('/')
def soen487_project():
    return jsonify({"title": "SOEN487 project",
                    "team": "ResoluteLeopards"})


if __name__ == '__main__':
    app.run()
