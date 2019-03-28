import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

photo_size = [56, 56]


def load_image(path):
    image_string = tf.io.read_file(path)
    image_decoded = tf.image.decode_png(image_string, channels=3)
    image_resized = tf.image.resize(image_decoded, photo_size)
    return image_resized


def predict_image(path):
    model = tf.keras.models.load_model('./cat_dog_classifier')
    image = load_image(path)
    predictions = model.predict(tf.stack([image]))
    return predictions[0][1]


prediction = predict_image('/home/psaid/Work/SOEN487-ResoluteLeopards/ml_api/lel/cats/cat.3550.jpg')
print(prediction)
