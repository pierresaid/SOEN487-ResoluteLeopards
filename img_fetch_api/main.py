from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

catApiUrl = "https://aws.random.cat/meow"
dogApiUrl = "https://random.dog/woof.json"

@app.route('/')
def root():
    return jsonify({"title": "Image Fetching API"})


@app.route('/cat')
def getRandomCat():
    url = requests.get(catApiUrl).json()['file']
    return jsonify({"url": url})


@app.route('/dog')
def getRandomDog():
    url = requests.get(dogApiUrl).json()['url']
    return jsonify({"url": url})


if __name__ == '__main__':
    app.run()
