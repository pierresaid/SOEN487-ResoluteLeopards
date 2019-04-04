from flask import Flask, jsonify, make_response
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

catApiUrl = "https://api.thecatapi.com/v1/images/search"
dogApiUrl = "https://random.dog/woof.json"


@app.route('/')
def root():
    return jsonify({"title": "Image Fetching API"})


def isValidImage(url):
    low = url.lower()
    return low.endswith('.png') or low.endswith('.jpg') or low.endswith('.jpeg')


@app.route('/cat')
def getRandomCat():
    try:
        while True:
            url = requests.get(catApiUrl).json()[0]['url']
            if isValidImage(url):
                break
        return jsonify({"url": url})
    except:
        print("[img_fetch_api]: Error in getRandomCat()")
        return make_response(jsonify({"url": None}), 500)

@app.route('/dog')
def getRandomDog():
    try:
        while True:
            url = requests.get(dogApiUrl).json()['url']
            if isValidImage(url):
                break
        return jsonify({"url": url})
    except:
        print("[img_fetch_api]: Error in getRandomDog()")
        return make_response(jsonify({"url": None}), 500)


if __name__ == '__main__':
    app.run()
