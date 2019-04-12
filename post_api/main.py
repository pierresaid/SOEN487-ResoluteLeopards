from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
from flask_cors import CORS
from common.auth import setup_auth

setup_auth('http://localhost:5001')
app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/*/*": {"origins": "*"}})

db = SQLAlchemy(app)

# since there is a circular dependency we have to put the import in the middle of the file
import post_models
import post_routes as pr

app.register_blueprint(pr.vote_blueprint)
app.register_blueprint(pr.post_blueprint)

app.config.from_object(DevConfig)

db.create_all()


@app.route('/')
def main_route():
    return jsonify({'code': 200, 'msg': 'You are on the post database api'})


@app.errorhandler(404)
def not_found_route(e):
    return jsonify({'code': 404, 'msg': '404: Not Found'}), 404


if __name__ == '__main__':
    app.run()
