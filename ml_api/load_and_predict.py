# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# print(tf.__version__)

cats_train_path = '/home/psaid/Work/SOEN487-ResoluteLeopards/ml_api/cats/'
cats_test_path = '/home/psaid/Work/SOEN487-ResoluteLeopards/ml_api/cats_test/'
dogs_train_path = '/home/psaid/Work/SOEN487-ResoluteLeopards/ml_api/dogs/'
dogs_test_path = '/home/psaid/Work/SOEN487-ResoluteLeopards/ml_api/dogs_test/'

from os import listdir
from os.path import isfile, join

class_names = ['Cat', 'Dog']

photo_size = [96, 96]


# photo_size = [16, 16]


def load_image(path):
    image_string = tf.io.read_file(path)
    image_decoded = tf.image.decode_png(image_string, channels=3)
    image_resized = tf.image.resize(image_decoded, photo_size)
    return image_resized


def _parse_function(filename, label=''):
    image_string = tf.io.read_file(filename)
    image_decoded = tf.image.decode_png(image_string, channels=3)
    image_resized = tf.image.resize(image_decoded, photo_size)
    # image_resized = tf.image.rgb_to_grayscale(image_resized)
    return image_resized


def path_to_dataset(paths, path_labels):
    non_tested_files = []
    temp_labels = []
    for idx, path in enumerate(paths):
        temp_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
        temp_labels += [path_labels[idx]] * len(temp_files)
        non_tested_files += temp_files

    files = []
    labels = []

    for idx, file in enumerate(non_tested_files):
        # try:
        image = _parse_function(file)
        files.append(image)
        labels.append(temp_labels[idx])
        # except:
        #     continue
    return files, tf.constant(labels)


# train_images, train_labels = path_to_dataset([cats_train_path, dogs_train_path], [0, 1])
test_images, test_labels = path_to_dataset([dogs_test_path, cats_test_path], [1, 0])
#
# train_images = [train_image / 255.0 for train_image in train_images]
test_images = [test_image / 255.0 for test_image in test_images]
#
# train_images = tf.stack(train_images)
test_images = tf.stack(test_images)


#
# IMG_SHAPE = (photo_size[0], photo_size[1], 3)




def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                         100 * np.max(predictions_array),
                                         class_names[true_label]),
               color=color)


def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array[i], true_label[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(2), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


model = tf.keras.models.load_model('./cat_dog_classifier')

predictions = model.predict(test_images)
print(predictions)


for i in range(10):
    plt.figure(figsize=(6,3))
    plt.subplot(1,2,1)
    plot_image(i, predictions, test_labels, test_images)
    plt.subplot(1,2,2)
    plot_value_array(i, predictions,  test_labels)
    plt.show()

def predict_image(path):
    image = load_image(path)
    predictions = model.predict(tf.stack([image]))
    return predictions[0][1]


# prediction = predict_image('/home/psaid/Work/SOEN487-ResoluteLeopards/ml_api/lel/cats/cat.3550.jpg')
# print(prediction)

# test_loss, test_acc = model.evaluate(test_images, test_labels)

# print('\nTest accuracy:', test_acc)
