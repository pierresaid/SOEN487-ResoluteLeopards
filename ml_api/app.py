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
    try:
        prediction = predict_image(url, model)
    except Exception:
        return make_response(jsonify({"message": 'Invalid url'}), 400)
    label = 'cat' if prediction < 0.5 else 'dog'
    percent = (100 - (prediction * 100)) if label == 'cat' else (prediction * 100)
    return make_response(jsonify({"label": label, "prediction":  f'{float(percent):.3f}'}), 200)


if __name__ == '__main__':
    app.run()
