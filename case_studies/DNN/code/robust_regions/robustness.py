#!./venv/bin/python3
import sys
sys.path.append("..")
import os, pickle
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import marabou_net
from marabou_net import MarabouNet, AllowedMisclassifications, Counterexample
from utils import _set_tf_log_level, ms_since_1970, _ms_to_human, create_dirpath
from clustering import LabelGuidedKMeansRegion
from scipy.spatial import distance


_set_tf_log_level()

DEFAULTS = dict(
    e_min=0.0,
    e_max=1.0,
    e_interval=0.0001,
    timeout=0,
    verbosity=1,
    marabou_verbosity=0,
    network_version=1
    )

class LocalRobustness():
    def __init__(
        self,
        network_path:str='',
        network_options:dict=dict(),
        experiment:str='safescad',
        X:np.array=np.array([]),
        Y:np.array=np.array([]),
        allowed_misclassifications:AllowedMisclassifications=None,
        e_min:float=DEFAULTS['e_min'],
        e_max:float=DEFAULTS['e_max'],
        e_interval:float=DEFAULTS['e_interval'],
        timeout:int=DEFAULTS['timeout'],
        verbosity:int=DEFAULTS['verbosity'],
        marabou_options:dict=dict(),
        marabou_verbosity:int=0
        ):
        assert len(network_path) > 0, 'network_path is required'
        assert X.shape[0] == Y.shape[0], 'X and Y must have same number of items'
        assert e_min < e_max, 'e_min must be less than or equal to e_max'
        self._network_path = network_path
        self._network_options = network_options
        self._X = X
        self._Y = Y
        self._allowed_misclassifications = allowed_misclassifications
        self._e_min = e_min
        self._e_max = e_max
        self._e_interval = e_interval
        self._timeout = timeout
        self._verbosity = verbosity
        self._marabou_options = marabou_options
        self._marabou_verbosity = marabou_verbosity
        self._results = None
        self._counterexamples = []

        net = getattr(marabou_net, f'{experiment}_Net')
        self._net = net(
            self._network_path,
            network_options=self._network_options,
            marabou_options=self._marabou_options,
            marabou_verbosity=self._marabou_verbosity
        )

    @property
    def net(self) -> MarabouNet:
        '''net property

        Returns:
            MarabouNet: the MarabouNet object
        '''
        return self._net

    @property
    def X(self) -> np.array:
        '''X property

        Returns:
            np.array: the verification inputs
        '''
        return self._X

    @property
    def Y(self) -> np.array:
        '''Y property

        Returns:
            np.array: the verification outputs
        '''
        return self._Y
    
    @property
    def dataset(self) -> Tuple[np.array, np.array]:
        '''dataset property (inputs and outputs)

        Returns:
            tuple(np.array, np.array): tuple containing (X, Y)
        '''
        return (self.X, self.Y)

    @property
    def results(self) -> pd.DataFrame:
        '''results property

        Returns:
            pd.DataFrame: returns a dataframe containing verification results
        '''
        return self._results

    @results.setter
    def results(self, results:pd.DataFrame):
        '''setter for results property

        Args:
            results (pd.DataFrame): a dataframe containing results
        '''
        self._results = results
    
    def get_counterexample(self, x_index:int) -> tuple:
        '''gets a counterexample from the sample @ x_index

        Args:
            x_index (int): index of sample in X

        Returns:
            np.array: returns the counterexample
        '''
        return self._counterexamples[x_index]

    def get_counterexamples(self, include_outputs=True) -> Dict[int, Counterexample]:
        '''returns all counterexamples (and optionally includes the outputs)

        Args:
            include_outputs (bool, optional): . Defaults to True.

        Returns:
            dict: dictionary containing counterexamples
        '''
        if include_outputs:
            return self._counterexamples
        return {k:c[0] for k,c in self._counterexamples.items()}
    counterexamples = property(get_counterexamples)

    @counterexamples.setter
    def counterexamples(self, counterexamples:dict):
        self._counterexamples = counterexamples
    
    def _find_counterexample(self, x:np.array, y:np.array, epsilon:float) -> tuple:
        lbs = x-epsilon
        ubs = x+epsilon
        for i in self.net.ignored_features:
            lbs[i] = x[i]
            ubs[i] = x[i]
        y_idx = np.argmax(y)
        return self.net.find_counterexample(lbs, ubs, y_idx,
            allowed_misclassifications=self._allowed_misclassifications,
            )
    
    def _get_predicted_label(self, actual_y, outputs:List[float]) -> int:
        maxval = max(outputs)
        for i in enumerate(outputs):
            if i != actual_y and i >= maxval:
                return i
        return actual_y

    def _find_epsilon(self, x:np.array, y:np.array, x_index=None) -> dict:
        lower, upper, interval = self._e_min, self._e_max, self._e_interval
        actual_label = np.argmax(y)
        predicted_label = actual_label
        epsilon = self._e_max
        counterexample = None
        while ((upper - lower) > interval):
            guess = lower + (upper - lower) / 2.0
            pred, cex = self._find_counterexample(x, y, guess)
            if self._verbosity > 1:
                print(f's{x_index}@epsilon={guess}: class={actual_label}, pred_class={pred}')
            if cex is None:
                # correct prediction
                lower = guess
            else:
                # incorrect prediction
                upper = guess
                epsilon = guess
                counterexample = cex
                predicted_label = pred
        return epsilon, predicted_label, counterexample
    
    def analyze(self, results_outpath:str='', counterexamples_outpath:str='', dataset_outpath:str=''):
        results, counterexamples = [], []
        X, Y = self.X, self.Y
        for i in range(X.shape[0]):
            x, y = X[i], Y[i]
            start = ms_since_1970()
            epsilon, pred_label, counterexample = self._find_epsilon(x, y, x_index=i)
            actual_label = np.argmax(y)
            duration = ms_since_1970() - start
            if self._verbosity > 0:
                print(f's{i}, class:{actual_label}, pred:{pred_label}, epsilon:{epsilon} ({duration} ms)')
            results.append({
                'x':i,
                'class': actual_label,
                'pred_class': pred_label,
                'epsilon':epsilon,
                'time':duration
                })
            counterexamples.append(counterexample)
        
        self.results = pd.DataFrame(results)
        self.counterexamples = counterexamples
        if self._verbosity > 0:
            print(f'completed analysis of {self.X.shape[0]} samples in {_ms_to_human(self.results["time"].sum())}')
        if results_outpath or counterexamples_outpath or dataset_outpath:
            self.save_results(results_outpath=results_outpath, counterexamples_outpath=counterexamples_outpath, dataset_outpath=dataset_outpath)
        return self

    def save_results(self, results_outpath:str='', counterexamples_outpath:str='', dataset_outpath:str=''):
        if results_outpath:
            create_dirpath(results_outpath)
            self.results.to_csv(results_outpath)
        if counterexamples_outpath:
            create_dirpath(counterexamples_outpath)
            pickle.dump(self.counterexamples, open(counterexamples_outpath, 'wb'))
        if dataset_outpath:
            create_dirpath(dataset_outpath)
            pickle.dump(self.dataset, open(dataset_outpath, 'wb'))
    
    def load_results(self, results_path:str='', counterexamples_path:str='', dataset_path:str=''):
        if results_path:
            self.results = pd.read_csv(results_path, index_col=0)
        if counterexamples_path:
            self.counterexamples = pickle.load(open(counterexamples_path, 'rb'))
        if dataset_path:
            self._X, self._Y = pickle.load(open(dataset_path, 'rb'))

def verify_regions(
    network_path:str='',
    network_options:dict=dict(),
    experiment:str='safescad',
    regions:List[LabelGuidedKMeansRegion]=[],
    e_min:float=DEFAULTS['e_min'],
    e_max:float=DEFAULTS['e_max'],
    e_interval:float=DEFAULTS['e_interval'],
    radius_padding:float=0,
    allowed_misclassifications=None,
    timeout:int=DEFAULTS['timeout'],
    marabou_options:dict=dict(),
    marabou_verbosity:int=0,
    out_dir:str='../../experiments/robust_regions'):
    # list to store verified regions
    vregions = []
    # verify regions one at a time...
    for i,region in enumerate(regions):
        # setup output paths for the region's robustness test
        region_outdir = f'{out_dir}/region_{i}'
        results_outpath = os.path.join(region_outdir, 'results.csv')
        counterexamples_outpath = os.path.join(region_outdir, 'counterexamples.p')
        
        # get the region's radius, centroid, number of features, and number of categories.
        radius, centroid, n_categories = region.radius, region.centroid, region.n_categories
        
        # setup the inputs for the robustness test (Xc=centroid, Yc=region's label)
        Xc, Yc = np.array([centroid]), np.array([[int(region.category==i) for i in range(n_categories)]])

        # setup the LocalRobustness object.
        lr = LocalRobustness(
            network_path=network_path,
            network_options=network_options,
            experiment=experiment,
            X=Xc,
            Y=Yc,
            e_min=e_min,
            e_max=e_max,
            e_interval=e_interval,
            allowed_misclassifications=allowed_misclassifications,
            timeout=timeout,
            marabou_options=marabou_options,
            marabou_verbosity=marabou_verbosity
            )
        # run the robustness test
        lr.analyze(
            results_outpath=results_outpath,
            counterexamples_outpath=counterexamples_outpath
            )
        # get the epsilon from the results, and use it to calculate the verified radius and density.
        region_results = lr.results.iloc[0]
        epsilon = region_results['epsilon']
        time = region_results['time']
        vradius = distance.euclidean(centroid + epsilon, centroid)
        density = region.n/vradius if vradius > 0 else region.n/e_interval
        region_data = {
            'centroid': region.centroid,
            'radius': vradius,
            'epsilon': epsilon,
            'n': region.n,
            'density': density,
            'category': region.category,
            'oradius': region.radius,
            'duration': time
        }
        vregions.append(region_data)
        print(f'region {i} - radius:{vradius}, epsilon: {epsilon}, ({time}ms)')

    # create a dataframe of all of the results.
    verified_regions = pd.DataFrame(vregions)
    vregions_file = os.path.join(out_dir, f'vregions.csv')
    create_dirpath(vregions_file)
    verified_regions.to_csv(vregions_file)
    print(f'Complete! Verified regions saved to: {vregions_file}')
    return verified_regions