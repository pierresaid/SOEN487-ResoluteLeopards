# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

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


# Reads an image from a file, decodes it into a dense tensor, and resizes it
# to a fixed shape.
def _parse_function(filename, label=''):
    image_string = tf.io.read_file(filename)
    image_decoded = tf.image.decode_jpeg(image_string)
    image_resized = tf.image.resize(image_decoded, [28, 28])
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
        try:
            image = _parse_function(file)
            files.append(image)
            labels.append(temp_labels[idx])
        except:
            continue
    return files, labels


train_images, train_labels = path_to_dataset([cats_train_path, dogs_train_path], [0, 1])
train_images = [train_image / 255.0 for train_image in train_images]
# test_dataset = path_to_dataset([cats_test_path, dogs_test_path], [0, 1])
# print(train_images)
# print(train_labels)

plt.figure(figsize=(10,10))
for i in range(1):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i])
    plt.xlabel(class_names[train_labels[i]])
plt.show()
