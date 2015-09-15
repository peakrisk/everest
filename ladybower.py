"""
Reservoir sampling
"""
import heapq

import numpy as np
from numpy import random

class WeightedReservoir(object):
    """ Sampling from a set of items with different weights.

    Simple usage
    ============

    Initialise with iterable of (weight, item) pairs.

    If you have the weights as a numpy array, then you
    can simply pass the weights to initialise_weights().
    This will avoid taking a copy of the weights.
    
    """
    
    def __init__(self, data=None, seed=0):
        """ Initialise sampler

        data: iterable with (weight, item) pairs.

        seed: random number seed.
        """
        # initialise the random state
        self.seed(seed)

        if data is None:
            return

        self.weights = np.zeroes(len(data))
    
    def seed(self, seed=0):
        """ Initialise RandomState """
        self.random = random.RandomState(seed)

    def initialise_weights(self, weights):
        """ Do prep work for weights

        
        """
        self.weights = weights

    def sample_without_replacement(self, k):
        """ Return a sample of size k, without replacement

        k < n

        O(n) + O(k)
        """
        pass
    
    def sample_with_replacement(self, k):
        """ Return a sample of size k, with replacement

        i.e. same item can be sampled more than once.
        """
