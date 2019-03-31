import tensorflow as tf
import os
import requests
from io import BytesIO
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

photo_size = [160, 160]


def load_image(url):
    response = requests.get(url)
    image_string = BytesIO(response.content).read()
    # image_string = urllib.urlopen(url)
    # image_string = tf.io.read_file(path)
    image_decoded = tf.image.decode_png(image_string, channels=3)
    image_resized = tf.image.resize(image_decoded, photo_size)
    return image_resized


def predict_image(path, model):
    try:
        image = load_image(path)
    except requests.exceptions.MissingSchema:
        return -1
    prediction = model.predict(tf.stack([image]))[0]
    return prediction

