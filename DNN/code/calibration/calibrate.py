import sys
sys.path.append("..")
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from data_preprocessing import get_data


# CALIBRATION LIBRARIES
import tensorflow_probability as tfp
from netcal.metrics import ECE
from netcal.scaling import TemperatureScaling
from netcal.presentation import ReliabilityDiagram
from scriptify import scriptify
from scipy.spatial import distance
from scipy.special import softmax

def calibrate(model, X_calibration, y_calibration, n_bins = 10):
    ##Using NetCal package
    confidences = softmax(model.predict(X_calibration), axis=-1)
    ece = ECE(n_bins)
    uncalibrated_score = ece.measure(confidences, y_calibration.argmax(axis=1))
    print("Calibration Error before calibration: ", uncalibrated_score)

    temperature = TemperatureScaling()
    temperature.fit(confidences, y_calibration.argmax(axis=1))
    calibrated = temperature.transform(confidences)
    calibrated_score = ece.measure(calibrated, y_calibration.argmax(axis=1))
    print("Calibration Error after calibration: ", calibrated_score)

    diagram = ReliabilityDiagram(n_bins)
    diagram.plot(confidences, y_calibration.argmax(axis=1))  # visualize miscalibration of uncalibrated

    diagram.plot(calibrated, y_calibration.argmax(axis=1))  # visualize miscalibration of calibrated
    return temperature

if __name__ == '__main__':

    @scriptify
    def script(experiment='safescad',
            conf_name='default'):
        '''
                    LOAD DATA
        '''
        data_dir = f'../../experiments/data/{experiment}/{conf_name}'
        model_dir = f'../../experiments/models/{experiment}/{conf_name}'

        X_train, y_train, X_calibration, y_calibration, X_confusion, y_confusion, X_test, y_test = get_data(experiment, None, data_dir)

        model = load_model(f'{model_dir}/model.h5')
        print("# of train samples: ", y_train.shape[0])
        print("# of test samples: ", y_test.shape[0])

        temperature_model = calibrate(model, X_calibration, y_calibration)
        temperature_model.save_model(f'{model_dir}/temperature_model')