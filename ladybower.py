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

    Alternatively, you can simply pass the weights to
    initialise_weights() and initialise_values()

    Or simply:

    >>> res = WeightedReservoir()
    >>> res.weights = weights
    >>> res.values = values
    
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

        # save data
        self.data = data

        # do initialisation for weights and values eg convert to numpy arrays
        self.initialise_weights(x[0] for x in data)
        self.initialise_values(x[1] for x in data)

    
    def seed(self, seed=0):
        """ Initialise RandomState """
        self.random = random.RandomState(seed)

    def initialise_weights(self, weights):
        """ Do prep work for weights
        """
        self.weights = np.array(weights)

    def isample_without_replacement(self, k):
        """ Return a sample of size k, without replacement

        k < n

        O(n)

        Use a heap to keep track of selection.
        """
        heap = []

        weights = 1.0 - (self.random(len(weights)) ** self.weights)

        for ix, weight in enumerate(weights):
            if ix < k:
                heapq.heapadd(heap, (weight, ix))
            else:
                if heap[0] < weight:
                    heapreplace(heap, (weight, ix))

        # now sort the heap -- this is to make things repeatable
        heap.sort()

        # return permuted indices
        return(self.random.permutation(x[0] for x in heap))
                    
        
    
    def isample_with_replacement(self, k):
        """ Return indices for a sample of size k, with replacement

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
        """ Return indices for a sample of size k, with replacement

        i.e. same item can be sampled more than once.
        """
        pass

    def sample_with_replacement(self, k):
        """ Return a sample of size k, with replacement

        i.e. same item can be sampled more than once.
        """
        return [self.data[x][1] for x in self.isample_with_replacement(k)]
    
