#Code copied from https://github.com/cmu-transparency/lib-gloro/blob/d6d01909ef82b711c4774e3895770955e131a5ce/gloro/smoothing/models.py
import json
import os
import shutil
import tarfile
import numpy as np
import tensorflow as tf
import tensorflow.keras.backend as K

from tensorflow.keras.models import Model

try:
    from tensorflow_probability.distributions import Normal
    from tensorflow_probability.distributions import Binomial
    from tensorflow_probability.distributions import Beta
except:
    from tensorflow_probability.python.distributions import Normal
    from tensorflow_probability.python.distributions import Binomial
    from tensorflow_probability.python.distributions import Beta

from math import ceil
from scipy.stats import norm, binom_test
from statsmodels.stats.proportion import proportion_confint


class SmoothedModel(Model):

    def __init__(
            self,
            inputs=None,
            outputs=None,
            model=None,
            sigma=1,
            alpha=0.001,
            n0=100,
            n=100000,
            noise_batchsize=64,
            epsilon=0.5,
            **kwargs):

        if model is None and (inputs is None or outputs is None):
            raise ValueError(
                'must specify either `inputs` and `outputs` or `model`')

        if model is not None and inputs is not None and outputs is not None:
            raise ValueError(
                'cannot specify both `inputs` and `outputs` and `model`')

        if inputs is None or outputs is None:
            inputs = model.inputs
            outputs = model.outputs

        else:
            model = Model(inputs, outputs)

        if not isinstance(outputs, (list, tuple)):
            outputs = [outputs]

        if len(outputs) > 1:
            raise ValueError(
                f'only models with a single output are supported, but got '
                f'{len(outputs)} outputs')

        super().__init__(inputs, outputs, **kwargs)

        self._n = n
        self._n0 = n0
        self._sigma = sigma
        self._alpha = alpha
        self._noise_batchsize = noise_batchsize
        self._epsilon = epsilon

        # We assume that this is a classifier with outputs of rank 2
        self._num_classes = outputs[0].shape[1]

        self._f = SmoothedModel.__ModelContainer(model)

    @property
    def f(self):
        return self._f.model

    @property
    def n0(self):
        return self._n0

    @n0.setter
    def n0(self, new_n0):
        self._n0 = new_n0

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, new_n):
        self._n = new_n

    @property
    def sigma(self):
        return self._sigma

    @sigma.setter
    def sigma(self, new_sigma):
        self._sigma = new_sigma

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, new_alpha):
        self._alpha = new_alpha

    @property
    def noise_batchsize(self):
        return self._noise_batchsize

    @noise_batchsize.setter
    def noise_batchsize(self, new_batchsize):
        self._noise_batchsize = new_batchsize

    @property
    def epsilon(self):
        return self._epsilon

    @epsilon.setter
    def epsilon(self, new_epsilon):
        self._epsilon = new_epsilon

    def _single_binom_test(self, x, n, p=0.5):

        dist = Binomial(total_count=n, probs=p)
        d = dist.prob(x)
        rerr = 1 + 1e-7
        if x < p * n:
            i = tf.range(tf.math.ceil(p * n), n + 1)
            y = tf.reduce_sum(tf.cast(dist.prob(i) <= d * rerr, tf.float32), axis=0)
            pval = dist.cdf(x) + dist.survival_function(n - y)
        else:
            i = tf.range(tf.math.floor(p * n) + 1)
            y = tf.reduce_sum(tf.cast(dist.prob(i) <= d * rerr, tf.float32), axis=0)
            pval = (dist.cdf(y - 1) + dist.survival_function(x - 1))

        return tf.math.minimum(1.0, pval)

    def _binom_test(self, x, n, p=0.5):

        return tf.map_fn(
            fn=lambda xn: self._single_binom_test(xn[0], xn[1], p=p),
            elems=(tf.cast(x, tf.dtypes.float32), tf.cast(n, tf.dtypes.float32)),
            dtype=tf.float32)
            # fn_output_signature=tf.float32)

    def _sample_model(self, x, n, training=False, **kwargs):
        x_batchsize = tf.shape(x)[0]

        counts = tf.zeros(
            (x_batchsize, self._num_classes),
            dtype=tf.dtypes.float32)

        for _ in range(ceil(n / self._noise_batchsize)):
            num = min(self._noise_batchsize, n)
            n -= num

            x_reps = tf.repeat(x, num, axis=0)
            noise = tf.random.normal(
                tf.shape(x_reps),
                stddev=self.sigma)
            ys = tf.one_hot(
                tf.argmax(self.f(x_reps + noise), axis=1),
                self._num_classes)
            ys_reduced = tf.map_fn(
                lambda w: tf.reduce_sum(ys[w:w + num], axis=0),
                tf.range(tf.shape(ys)[0], delta=num),
                dtype=tf.dtypes.float32)
                # fn_output_signature=tf.dtypes.float32)

            counts += ys_reduced

        return counts

    def call(self, x, training=False, **kwargs):

        counts = self._sample_model(x, self.n0, training=training, **kwargs)
        top2 = tf.math.top_k(counts, k=2)

        x_test = top2.values[:, 0]
        n_test = x_test + top2.values[:, 1]
        pvals = self._binom_test(x_test, n_test)

        ys = tf.where(
            pvals <= self.alpha,
            top2.indices[:, 0],
            self._num_classes + tf.zeros(tf.shape(x)[0], dtype=tf.int32))

        return tf.one_hot(ys, self._num_classes + 1)

    def predict_prob(self, x):
        return self._sample_model(x, self.n0, training=False) / self.n0

    def _single_lower_confidence_bound(self, n_success, n_total, alpha=0.5):

        if n_success == 0:
            return tf.constant(0, tf.dtypes.float32)
        else:
            # tfp hasn't implemented the quantile function yet!
            # return Beta(n_success, n_success-n_total+1).quantile(alpha)
            return proportion_confint(n_success, n_total, alpha=2 * alpha, method='beta')[0]

    def certify(self, x):
        x = tf.cast(x, tf.float32)
        select = self._sample_model(x, self.n0, training=False)
        guess = tf.argmax(select, axis=1)
        estimate = self._sample_model(x, self.n, training=False)
        n_guess = tf.gather(estimate, guess, batch_dims=1)

        confidence = tf.map_fn(
            fn=lambda n_guess_i: self._single_lower_confidence_bound(n_guess_i, self.n, alpha=self.alpha),
            elems=n_guess)

        ys = tf.where(confidence < 0.5, self._num_classes, guess)
        eps = tf.where(confidence < 0.5, 0., self.sigma * Normal(0, 1).quantile(confidence))

        return (ys, eps)

    def vra(self, x, y, epsilon):
        # assuming sparse encoding for y
        ys, radii = self.certify(x)

        return tf.reduce_mean(
            tf.cast(tf.equal(tf.argmax(ys, axis=1), y), 'float32') *
            tf.cast(radii >= epsilon))

    def get_config(self):
        return {
            'n': int(self.n),
            'n0': int(self.n0),
            'sigma': float(self.sigma),
            'alpha': float(self.alpha),
            'noise_batchsize': int(self.noise_batchsize),
            'epsilon': float(self.epsilon)
        }

    def save(self, file_name):
        if file_name.endswith('.rs'):
            file_name = file_name[:-3]

        try:
            os.mkdir(file_name)

            self.f.save(f'{file_name}/f.h5')

            with open(f'{file_name}/config.json', 'w') as json_file:
                json.dump(self.get_config(), json_file)

            with tarfile.open(f'{file_name}.rs', 'w:gz') as tar:
                tar.add(file_name, arcname=os.path.basename(file_name))

        finally:
            shutil.rmtree(file_name)

    @staticmethod
    def load_model(file_name):
        if file_name.endswith('.rs'):
            file_name = file_name[:-3]

        temp_dir = f'{file_name}___'

        try:
            os.mkdir(temp_dir)

            with tarfile.open(f'{file_name}.rs', 'r:gz') as tar:

                for member in tar:
                    if member.name.endswith('.h5'):
                        tar.extract(member, f'{temp_dir}')

                        model = tf.keras.models.load_model(
                            f'{temp_dir}/{member.name}')

                    elif member.name.endswith('.json'):
                        with tar.extractfile(member) as f:
                            config = json.load(f)
        finally:
            shutil.rmtree(temp_dir)

        return SmoothedModel(
            model=model,
            n=config['n'],
            n0=config['n0'],
            sigma=config['sigma'],
            alpha=config['alpha'],
            noise_batchsize=config['noise_batchsize'],
            epsilon=config['epsilon'])

    class __ModelContainer(object):
        def __init__(self, model):
            self.model = model