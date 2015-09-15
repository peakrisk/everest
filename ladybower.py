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

    Sampling
    ========
    isample_with[out]_replacement() -- samples with[out] replacement,
                                       returns indices of values to
                                       select

    sample_with[out]_replacement()  -- samples with[out] replacement,
                                       returns values to select
    
    
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

        self.weights = np.array(x[0] for x in data)
        self.values = [x[1] for x in data]

        # dilemma: return indices of elements to select, or values?
        # solution:  return indices, but have a routine that returns values.
    
    def seed(self, seed=0):
        """ Initialise RandomState """
        self.random = random.RandomState(seed)

    def initialise_weights(self, weights):
        """ Do prep work for weights

        
        """
        self.weights = weights

    def isample_without_replacement(self, k):
        """ Return a sample of size k, without replacement

        k < n

        O(n)

        Use a heap to keep track of selection.
        """
        heap = 
    
    def isample_with_replacement(self, k):
        """ Return a sample of size k, with replacement

        i.e. same item can be sampled more than once.
        """
        pass

    def sample_without_replacement(self, k):
        """ Return a sample of size k, without replacement

        k < n

        O(n)

        Use a heap to keep track of selection.
        """
        return [self.data[x][1] for x in self.isample_without_replacement(k)]
    
    def isample_with_replacement(self, k):
        """ Return a sample of size k, with replacement

        i.e. same item can be sampled more than once.
        """
        pass

    def sample_with_replacement(self, k):
        """ Return a sample of size k, with replacement

        i.e. same item can be sampled more than once.
        """
        return [self.data[x][1] for x in self.isample_with_replacement(k)]
    
