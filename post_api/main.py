from flask import Flask, jsonify
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

# since there is a circular dependency we have to put the import in the middle of the file
import routes

app.register_blueprint(routes.vote_blueprint)
app.register_blueprint(routes.post_blueprint)

db.create_all()


@app.route('/')
def main_route():
    return jsonify({'code': 200, 'msg': 'You are on the post database api'})


if __name__ == '__main__':
    app.run()
