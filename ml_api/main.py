from flask import Flask, jsonify, make_response, request

from classifier import predict_image
from flask_cors import CORS
import tensorflow as tf

app = Flask(__name__)
CORS(app)

prediction_names = ['cat', 'dog']

model = tf.keras.models.load_model('./cat_dog_classifier')


@app.route('/')
def root():
    return jsonify({"title": "Prediction API"})


@app.route('/predict')
def predict_for_url():
    url = request.args.get('url')
    if not url:
        return make_response(jsonify({"message": 'Missing url'}), 400)
    prediction = predict_image(url, model)
    if prediction == -1:
        return make_response(jsonify({"message": 'Invalid url'}), 400)
    return make_response(jsonify({"prediction": 'cat' if prediction < 0.5 else 'dog'}), 200)


if __name__ == '__main__':
    app.run()
