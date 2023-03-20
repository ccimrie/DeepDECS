import sys
sys.path.append("..")
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model

from scriptify import scriptify
from data_preprocessing import get_data
from netcal.scaling import TemperatureScaling
from rs.smoothed_model import SmoothedModel
from gloro.models import GloroNet
from time import time
from scipy.special import softmax

class RobustRegions:
    def __init__(self, experiment, conf_name, num_features):
        centroids = []
        l2_radii = []
        linf_radii = []
        robust_regions_dir = f'../experiments/robust_regions/{experiment}/{conf_name}'
        verified_regions_data = pd.read_csv(f'{robust_regions_dir}/vregions.csv')
        for index, row in verified_regions_data.iterrows():
            l2_radii.append(row['radius'])
            linf_radii.append(row['epsilon'])
            centroids_row = []
            for i in range(0, num_features):
                centroids_row.append(row[f'cx{i}'])
            centroids.append(np.array(centroids_row))

        self.zip_centroids_linf_radii = zip(centroids,linf_radii)
        self.zip_centroids_l2_radii = zip(centroids,l2_radii)

    def isVerified(self, x, y_pred, y):
        for (centroid, linf_radius) in self.zip_centroids_linf_radii:
            # if distance.euclidean(x, centroid) <= l2_radius:
            if ((centroid - linf_radius) <= x) and (x <= (centroid + linf_radius)):
                return True
        return False

class Confidence:
    def __init__(self, model_dir, threshold):
        # calibrated_data = pd.read_csv(f'{data_dir}/test_calibrated.csv', header=None)
        self.temperature_model = TemperatureScaling()
        self.temperature_model.load_model(f'{model_dir}/temperature_model')
        self.threshold = threshold

    def isVerified(self, x, pred):
        y_calibrated = self.temperature_model.transform(pred)
        pred_label = np.argmax(pred, axis=1)

        # In the case of binary classification, transform() only returns the probability
        # of the second label. Hence, we have to make the following modifications
        if pred.shape[1] == 2:
            y_calibrated_1 = np.ones(y_calibrated.shape, dtype=y_calibrated.dtype)
            y_calibrated_1 = y_calibrated_1 - y_calibrated
            y_calibrated = np.concatenate((np.expand_dims(y_calibrated_1,axis=1),
                                           np.expand_dims(y_calibrated,axis=1)), axis=1)
        ver_outcome = y_calibrated[np.arange(len(pred_label)), pred_label] >= self.threshold
        return ver_outcome

class RandomizedSmoothing:
    def __init__(self, model_dir):
        self.g = SmoothedModel.load_model(f'{model_dir}/model.rs')
        self.epsilon = self.g.epsilon

    def isVerified(self, x, pred):
        pred_label, eps = self.g.certify(x)
        ver_outcome = eps >= self.epsilon
        return ver_outcome.numpy()

class GloRo:
    def __init__(self, model, epsilon):
        self.g = GloroNet(model=model, epsilon=epsilon)
        self.epsilon = epsilon

    def isVerified(self, x, pred):
        pred_label, eps, _ = self.g.predict_with_certified_radius(x)
        ver_outcome = eps >= self.epsilon
        return ver_outcome.numpy()


if __name__ == '__main__':

    @scriptify
    def script(experiment='safescad',
               conf_threshold=0.7,
               epsilon=0.5,
               conf_name='default',
               num_verification_methods=2):
        print("Configuration Options:")
        print("experiment=",experiment)
        print("conf_threshold=",conf_threshold)
        print("epsilon=",epsilon)
        print("conf_name=",conf_name)


        data_dir = f'../experiments/data/{experiment}/{conf_name}'
        model_dir = f'../experiments/models/{experiment}/{conf_name}'
        confusion_dir = f'../experiments/confusion_matrices/{experiment}/{conf_name}'

        if not os.path.exists(confusion_dir):
            os.makedirs(confusion_dir)

        # LOAD DATA
        _, _, _, _, X_confusion, y_confusion, _, _ = get_data(experiment, None, data_dir)
        num_features = X_confusion.shape[1]
        num_classes = y_confusion.shape[1]
        print("# of samples for confusion matrices generation: ", X_confusion.shape[0])

        # Load model
        model = load_model(f'{model_dir}/model.h5')

        # Setup data structures
        eval_start_time = time()
        y_pred = softmax(model.predict(X_confusion), axis=-1)
        eval_time = time() - eval_start_time
        verif_time = 0
        num_verified = np.zeros((2 ** num_verification_methods))
        confusion_matrices = []
        for i in range(0, 2 ** num_verification_methods):
            confusion_matrices.append(np.zeros((num_classes, num_classes)))

        # Setup verification methods
        v0 = GloRo(model, epsilon)
        v1 = Confidence(model_dir, conf_threshold)
        # v2 = RobustRegions(experiment, conf_name, num_features)
        # v3 = RandomizedSmoothing(model_dir)
        v = [v0, v1]

        eval_samples = X_confusion.shape[0]
        eval_batch_size = 128
        for index in range(eval_samples // eval_batch_size):
            print(f'Iteration {index} of {eval_samples // eval_batch_size}')
            strt_indx = index * eval_batch_size
            end_indx = (index + 1) * eval_batch_size if (index + 1 < (eval_samples // eval_batch_size)) \
                else eval_samples
            x, y = X_confusion[strt_indx:end_indx, ], y_confusion[strt_indx:end_indx, ]
            pred = y_pred[strt_indx:end_indx, ]
            pred_label = np.argmax(pred, axis=1)
            act_label = np.argmax(y, axis=1)
            conf_idx = np.zeros(pred_label.shape, dtype=int)

            for v_idx in range(0, num_verification_methods):
                verif_start_time = time()
                v_res = v[v_idx].isVerified(x, pred)
                verif_time += time() - verif_start_time
                conf_idx = conf_idx + v_res.astype(int) * (2 ** v_idx)

            #update confusion matrices
            for j in range(conf_idx.shape[0]):
                confusion_matrices[conf_idx[j]][act_label[j]][pred_label[j]] += 1
                num_verified[conf_idx[j]] += 1

        print('# of test samples', X_confusion.shape[0])
        print("# of test samples in each combination of verification outcomes: ", num_verified)
        print('Total time to evaluate in seconds:', eval_time)
        print('Total time to verify in seconds:', verif_time)

        for idx in range(0, 2**num_verification_methods):
            b_idx = "{0:02b}".format(idx)
            confusion_fname = f'{confusion_dir}/conf_{b_idx}'
            with open(confusion_fname, 'w') as f:
                print(confusion_matrices[idx], file=f)



