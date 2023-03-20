import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn import metrics
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from scriptify import scriptify
import architectures
from utils import setup_nnet_tools, compute_nnet_params, save_nnet
from data_preprocessing import get_data
from rs.smoothed_model import SmoothedModel
from calibration.calibrate import calibrate
from gloro.models import GloroNet
from gloro.training import losses
from gloro.training.callbacks import EpsilonScheduler
from gloro.training.callbacks import LrScheduler
from gloro.training.metrics import clean_acc
from gloro.training.metrics import vra
from gloro.training.metrics import rejection_rate

def print_training_stats(history, saved_model_dir, n_categories, saved_model, X_test_enc, y_test_enc):
    # plot training history
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend(['train', 'test'], loc='upper left')
    plt.ylabel('Loss')
    plt.savefig(f'{saved_model_dir}/training_history.png', dpi=300)
    plt.show()

    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig(f'{saved_model_dir}/accuracy_history.png', dpi=300)
    plt.show()

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig(f'{saved_model_dir}/loss_history.png', dpi=300)
    plt.show()

    # note in kera model.predict() will return predict probabilities
    pred_prob = saved_model.predict(X_test_enc, verbose=0)
    fpr, tpr, threshold = metrics.roc_curve(y_test_enc.ravel(), pred_prob.ravel())
    roc_auc = metrics.auc(fpr, tpr)

    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_categories):
        fpr[i], tpr[i], _ = metrics.roc_curve(y_test_enc[:, i], pred_prob[:, i])
        roc_auc[i] = metrics.auc(fpr[i], tpr[i])

        # Compute micro-average ROC curve and ROC area
    fpr['micro'], tpr['micro'], _ = metrics.roc_curve(y_test_enc.ravel(), pred_prob.ravel())
    roc_auc['micro'] = metrics.auc(fpr['micro'], tpr['micro'])

    # Compute macro-average ROC curve and ROC area
    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(3)]))

    # Then interpolate all ROC curves at this points
    mean_tpr = np.zeros_like(all_fpr)
    for i in range(n_categories):
        mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])

    # Finally average it and compute AUC
    mean_tpr /= n_categories

    fpr['macro'] = all_fpr
    tpr['macro'] = mean_tpr
    roc_auc['macro'] = metrics.auc(fpr['macro'], tpr['macro'])

    plt.figure(1)
    plt.plot(fpr['micro'], tpr['micro'],
             label='micro-average ROC curve (area = {0:0.2f})' \
                   ''.format(roc_auc['micro']),
             color='deeppink', linestyle=':', linewidth=4)

    plt.plot(fpr['macro'], tpr['macro'],
             label='macro-average ROC curve (area = {0:0.2f})' \
                   ''.format(roc_auc['macro']),
             color='navy', linestyle=':', linewidth=4)

    colors = cycle(['aqua', 'darkorange', 'cornflowerblue', 'red', 'blue'])
    for i, color in zip(range(n_categories), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=2,
                 label='ROC curve of class {0} (area = {1:0.2f})' \
                       ''.format(i, roc_auc[i]))

    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Result for Receiver operating characteristic to multi-class of Reaction Time')
    plt.legend(loc='lower right')
    plt.savefig(f'{saved_model_dir}/roc.png', dpi=300)
    plt.show()

if __name__ == '__main__':

    @scriptify
    def script(experiment='safescad',
               epochs=30,
               batch_size=128,
               dataset_file=None,
               conf_name='default',
               noise=None,
               epsilon=0.5,
               lr=0.01,
               gloro='Y',
               gpu=0):
        print("Configuration Options:")
        print("experiment=", experiment)
        print("epochs=", epochs)
        print("batch_size=", batch_size)
        print("dataset_file=", dataset_file)
        print("conf_name=", conf_name)
        print("noise=", noise)
        print("epsilon=", epsilon)
        print("lr=", lr)
        print("gloro=", gloro)


        # Select the GPU and allow memory growth to avoid taking all the RAM.
        gpus = tf.config.experimental.list_physical_devices('GPU')
        tf.config.experimental.set_visible_devices(gpus[gpu], 'GPU')
        device = gpus[gpu]

        for device in tf.config.experimental.get_visible_devices('GPU'):
            tf.config.experimental.set_memory_growth(device, True)

        #Basic setup and install additional dependencies
        # Some global variables and general settings
        model_dir = f'../experiments/models/{experiment}/{conf_name}'
        data_dir = f'../experiments/data/{experiment}/{conf_name}'
        pd.options.display.float_format = '{:.2f}'.format
        nnet_tools_path = os.path.abspath('NNet')

        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # setup nnet tools (for converting model to Stanford's nnet format)
        setup_nnet_tools(nnet_tools_path)

        # Load and Preprocess Dataset
        X_train_enc, y_train_enc, X_calibration_enc, y_calibration_enc, X_confusion_enc, y_confusion_enc, \
        X_test_enc, y_test_enc = get_data(experiment, dataset_file, data_dir, noise=noise)

        ## Build & Train NN
        n_categories = y_train_enc.shape[1]
        arch = getattr(architectures, f'arch_{experiment}')
        model = arch((X_train_enc.shape[1],), classes=n_categories)

        if gloro == 'N':
            # training callbacks
            es_cb = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=30)
            # mc_file = 'model-best-{epoch:02d}-{val_loss:.2f}.h5'
            # mc_cb = ModelCheckpoint(mc_file, monitor='val_accuracy', verbose=1, save_best_only=True)
            # tb_cb = TensorBoard(log_dir=tensorboard_logs, histogram_freq=1, write_graph=True, write_images=True)
            reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=15, min_lr=0.0001)


            optimizer = tf.keras.optimizers.SGD(learning_rate=lr)
            # optimizer = tf.keras.optimizers.Adam(learning_rate=0.02)
            model.compile(loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True), optimizer=optimizer, metrics=['accuracy'])
            model.summary()

            # fit the keras model on the dataset
            history = model.fit(X_train_enc, y_train_enc,
                                validation_data=(X_calibration_enc, y_calibration_enc),
                                epochs=epochs,
                                batch_size=batch_size,
                                callbacks=[es_cb, reduce_lr])
            # callbacks=[es_cb, mc_cb, tb_cb])

            # evaluate the model
            print('Evaluating model ...')
            _, train_acc = model.evaluate(X_train_enc, y_train_enc, verbose=2)
            _, test_acc = model.evaluate(X_test_enc, y_test_enc, verbose=1)
            print('Accuracy of test: %.2f' % (test_acc * 100))
            print('Accuracy of the: ' + '1) Train: %.3f, 2) Test: %.3f' % (train_acc, test_acc))

        elif gloro == 'Y':

            gloro_model = GloroNet(model=model, epsilon=epsilon, num_iterations=5)
            gloro_model.summary()
            gloro_model.compile(
                loss=losses.get('crossentropy'),
                optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
                metrics=[clean_acc, vra, rejection_rate])

            history = gloro_model.fit(X_train_enc, y_train_enc,
                                      validation_data=(X_calibration_enc, y_calibration_enc),
                                      epochs=epochs,
                                      batch_size=batch_size,
                                      callbacks=[EpsilonScheduler('fixed'),
                                                 LrScheduler('decay_to_0.0001'),])

            # evaluate the model
            print('Evaluating model ...')
            train_eval = gloro_model.evaluate(X_train_enc, y_train_enc)
            test_eval = gloro_model.evaluate(X_test_enc, y_test_enc)
            results = {}
            results.update({
                'test_' + metric.name.split('pred_')[-1]: round(value, 4)
                for metric, value in zip(gloro_model.metrics, test_eval)
            })
            results.update({
                'train_' + metric.name.split('pred_')[-1]: round(value, 4)
                for metric, value in zip(gloro_model.metrics, train_eval)
            })
            print(results)

            model = gloro_model.f



        # save model in tf and h5 formats
        tf_model_path = f'{model_dir}/model.tf'
        h5_model_path = f'{model_dir}/model.h5'
        model.save(tf_model_path)  # save_format='tf'
        model.save(h5_model_path, save_format='h5')


        # extract params for nnet format
        nnet_params = compute_nnet_params(tf_model_path, np.concatenate((X_train_enc,X_test_enc)))
        weights, biases, input_mins, input_maxs, means, ranges = nnet_params

        # write the model to nnet file. Note that the final softmax operation is not recorded in the nnet file.
        # This does not affect any of the verification queries we pose to Marabou.
        nnet_path = os.path.join(model_dir, f'model.nnet')
        save_nnet(weights, biases, input_mins, input_maxs, means, ranges, nnet_path)

        #print_training_stats(history, model_dir, n_categories, model, X_test_enc, y_test_enc)

        ## calibrate model
        temperature_model = calibrate(model, X_calibration_enc, y_calibration_enc)
        temperature_model.save_model(f'{model_dir}/temperature_model')

        # evaluate randomized smoothing model
        if noise is not None:
            g = SmoothedModel(model=model, sigma=noise, epsilon=epsilon, n=10000)
            g.save(f'{model_dir}/model.rs')

            all_preds = []
            all_eps = []
            all_correct = []
            eval_samples = X_test_enc.shape[0]
            eval_batch_size = batch_size
            for index in range(eval_samples // eval_batch_size):
                print(f'Randomized smoothing evaluation: Iteration {index} of {eval_samples // eval_batch_size}')
                strt_indx = index * eval_batch_size
                end_indx = (index + 1) * eval_batch_size if (index + 1 < (eval_samples // eval_batch_size)) \
                    else eval_samples
                x,y = X_test_enc[strt_indx:end_indx,], y_test_enc[strt_indx:end_indx,]
                preds, eps = g.certify(x)
                all_preds.append(preds.numpy())
                all_eps.append(eps.numpy())
                all_correct.append(preds.numpy() == np.argmax(y,axis=1))


            preds = np.concatenate(all_preds, axis=0)
            eps = np.concatenate(all_eps, axis=0)
            correct = np.concatenate(all_correct, axis=0)

            clean_acc_res = correct.mean()
            vra_res = (correct * (eps >= epsilon)).mean()
            rejection_rate_res = (preds == n_categories).mean()

            print('Randomized Smoothing model results:\n'
                f'clean_acc:      {clean_acc_res:.3f}\n'
                f'vra:            {vra_res:.3f}\n'
                f'rejection_rate: {rejection_rate_res:.3f}\n')

