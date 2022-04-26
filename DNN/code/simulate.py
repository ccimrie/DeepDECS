import os, time
from make_verified_prediction import VerifiedPredict
from netcal.scaling import TemperatureScaling
import numpy as np
from tensorflow.keras.models import load_model
from pickle import load
from threading import Thread
import sys

data_no_collision=np.loadtxt('../../../../data_buckets/no_collision_v3.txt')
data_collision=np.loadtxt('../../../../data_buckets/collision_v3.txt')

# collision=int(sys.argv[1])
# ind=int(sys.argv[2])

#main loop
class mainLoop(Thread):
    def run(self):
        params = {
            'DNNmodel_path': '../experiments/models/collision/model.h5',
            'Temperature_model_path': '../experiments/models/collision/temperature_model',
            'scaler_path': '../experiments/models/collision/scaler',
            'epsilon': 0.05,
            'conf_threshold': 0.8
        }

        # Initialization
        print(params)
        print("loading models ...")
        model = load_model(params['DNNmodel_path'])
        temperature_model = TemperatureScaling()
        temperature_model.load_model(params['Temperature_model_path'])
        # scaler = load(open(params['scaler_path'], 'rb'))
        verified_predictor = VerifiedPredict(model, temperature_model, params['epsilon'], params['conf_threshold'])

        # while True:
            # time.sleep(1)

        filename_collision='../../../../data_buckets/collision_predictions_v3.txt'
        filename_no_collision='../../../../data_buckets/no_collision_predictions_v3.txt'

        open(filename_no_collision, 'w').close()
        open(filename_collision, 'w').close()

        for i in np.arange(len(data_no_collision)):
            # X_test = self.read_data(params)
            if i%100==0:
                print(i)
            X_test=np.reshape(data_no_collision[i,:],(1,5))
            (pred_label, v0, v1) = verified_predictor.make_verified_prediction(X_test)
            with open(filename_no_collision, 'a') as out:
                out.write(str(pred_label[0]) + ' ' + str(v0[0]) + ' ' + str(v1[0]) + '\n')

        for i in np.arange(len(data_collision)):
            # X_test = self.read_data(params)
            if i%1000==0:
                print(i)
            X_test=np.reshape(data_collision[i,:],(1,5))
            (pred_label, v0, v1) = verified_predictor.make_verified_prediction(X_test)
            with open(filename_collision, 'a') as out:
                out.write(str(pred_label[0]) + ' ' + str(v0[0]) + ' ' + str(v1[0]) + '\n')
            #TODO: send the triple to the simulator


    # Receive data from the simulator
    def read_data(self,params):
        #TODO: Receive data from the simulator
        X_test = np.zeros([1,5])
        return X_test

################################################################MAINFUNC
def main():
    mainLoop().start()
    # print("YIPPEE")


if __name__ == "__main__":
    main()

