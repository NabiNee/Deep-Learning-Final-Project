import socket
import cv2
import os
import tqdm
import io
import pandas as pd
import numpy as np
import csv
from scipy.io import loadmat
import tensorflow as tf
from tensorflow.keras import models

import json
from flask import Flask, jsonify
from flask import request
#import joblib
from datetime import date

import numpy as np
from PIL import Image

from socket import *

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(5)


BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
from datetime import date

print ('The server is ready to receive')
while 1:
    connectionSocket, addr = serverSocket.accept()
    print ('Connection Recieved')
    sentence = connectionSocket.recv(1024).decode()
    sentencelower = sentence.lower()
    if (sentencelower == 'get'):
        today = date.today()
        sentence = 'Alex Hom\nJulian Geske\nJordan Nienaber\nJJA Car Model Classification Server\n' + str(today)
    elif (sentencelower == 'post'):
        recieved = connectionSocket.recv(BUFFER_SIZE).decode()
        filename, filesize = recieved.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True,unit_divisor=1024)
        with open(filename, "wb") as f:
            for _ in progress:
                bytes_read = connectionSocket.recv(BUFFER_SIZE)
                if len(bytes_read) < BUFFER_SIZE:
                    print("\nFile Successfully Delivered")
                    f.write(bytes_read)
                    progress.update(len(bytes_read))
                    break
                if not bytes_read:
                    print("\nFile Successfully Delivered")
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))
#open image, convert to tensor, normalize, resize, turn to array
        test_image = np.asarray(Image.open(filename))
        test_image = test_image/255.0
        test_image = tf.image.resize_with_pad(test_image, target_height = 200, target_width = 200)
        test_image_list = np.array([test_image])
#load model, make prediction, convert output
        Car_model = tf.keras.models.load_model('JJA_CarRec_v1.h5')
        Model_prediction = Car_model.predict(test_image_list, batch_size = 1)
        Model_prediction_value = np.where(Model_prediction[0] == np.amax(Model_prediction[0]))
        Model_prediction_value = Model_prediction_value[0]
#decompile, opencsv, load translations
        prepared_prediction = Model_prediction_value.item(0)
        with open('JJA_Cars_Model_prediction_decoder.csv') as csv_file:
                reader = csv.reader(csv_file)
                labels = dict(reader)
        Predicted_car = labels.get(str(prepared_prediction))
        Predicted_car = int(Predicted_car)
        meta_data_path_translation = os.path.join(os.getcwd() + "\cars_meta.mat")
        meta_data_translation = loadmat(meta_data_path_translation)
#translate the translator, convert to dictionary
        dat_temp = [[row.flat[0] for row in line] for line in meta_data_translation['class_names'][0]]
        col_temp = ['class_names']
        df_train_meta_translation = pd.DataFrame(dat_temp, columns = col_temp)
        Car_translation_Dict = pd.DataFrame.to_dict(df_train_meta_translation)
        Car_translation_Dict = Car_translation_Dict['class_names']
#prep return string
        today = date.today()
        sentence = 'Alex Hom\nJulian Geske\nJordan Nienaber\n' + str(today) + '\nYour Vehicle: ' + str(Car_translation_Dict.get(Predicted_car))
    connectionSocket.send(sentence.encode())
    print('Connection Closed')
    connectionSocket.close()
    sentencelower = ' '
