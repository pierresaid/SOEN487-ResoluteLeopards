from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def get_root_page():
    return jsonify({"Hello": "World"})


if __name__ == "__main__":
    app.run()
