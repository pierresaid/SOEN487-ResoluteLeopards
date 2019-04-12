from flask import Flask, jsonify, make_response
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

post_api_url = "http://localhost:5000/"

@app.route('/')
def root():
    return jsonify({"title": "Analytics API"}), 200


@app.route('/results')
def results():
    votes = requests.get(post_api_url + 'vote').json()
    if (votes):
        dogs_vote_nb = len([v['value'] for v in votes if v['value'] == '0'])
        cats_vote_nb = len([v['value'] for v in votes if v['value'] == '1'])
        total = dogs_vote_nb + cats_vote_nb        
    if (votes and total is not 0):
        dogs_percent = dogs_vote_nb / total * 100
        cats_percent = cats_vote_nb / total * 100
        return make_response(jsonify({"cats": cats_percent, "dogs": dogs_percent}), 200)
    return make_response(jsonify({"cats": 0, "dogs": 0}), 200)


if __name__ == '__main__':
    app.run()
