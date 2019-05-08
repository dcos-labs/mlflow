#!/usr/bin/env python
# coding: utf-8

import tensorflow as tf
from tensorflow import keras
import numpy as np
import json
import os
import subprocess
import time
import tempfile
import mlflow
import mlflow.tensorflow

if __name__ == "__main__":
    with mlflow.start_run():
        fashion_mnist = keras.datasets.fashion_mnist
        (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

        train_images = train_images / 255.0
        test_images = test_images / 255.0

        train_images = train_images.reshape(train_images.shape[0], 28, 28, 1)
        test_images = test_images.reshape(test_images.shape[0], 28, 28, 1)

        class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                       'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

        print('\ntrain_images.shape: {}, of {}'.format(train_images.shape, train_images.dtype))
        print('test_images.shape: {}, of {}'.format(test_images.shape, test_images.dtype))

        model = keras.Sequential([
          keras.layers.Conv2D(input_shape=(28,28,1), filters=8, kernel_size=3, 
                              strides=2, activation='relu', name='Conv1'),
          keras.layers.Flatten(),
          keras.layers.Dense(10, activation=tf.nn.softmax, name='Softmax')
        ])
        model.summary()

        testing = False
        epochs = 5

        model.compile(optimizer=tf.train.AdamOptimizer(), 
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(train_images, train_labels, epochs=epochs)

        test_loss, test_acc = model.evaluate(test_images, test_labels)
        print('\nTest accuracy: {}'.format(test_acc))

        MODEL_NAME = 'mnist'
        MODEL_DIR = './' + MODEL_NAME
        MODEL_VERSION = str(int(time.time()))
        export_path = os.path.join(MODEL_DIR, str(MODEL_VERSION))
        print('export_path = {}\n'.format(export_path))
        if os.path.isdir(export_path):
          print('\nAlready saved a model, cleaning up\n')
          get_ipython().system('rm -r {export_path}')

        tf.saved_model.simple_save(
            keras.backend.get_session(),
            export_path,
            inputs={'input_image': model.input},
            outputs={t.name:t for t in model.outputs})
