""" Lady Bower tests """
import unittest
from unittest.mock import Mock

import collections

from everest import ladybower

class TestWeightedReservoit(unittest.TestCase):

    def test_isample_without_replacement(self):
        """ """
        data = [(x + 1, x) for x in range(200)]

        res = ladybower.WeightedReservoir(data, seed=0)

        counter = collections.Counter()
        
        for trial in range(1000):
            sample = res.isample_without_replacement(10)

            counter.update(sample)

        print(counter)
        
        self.assertTrue(([x for x in range(10)] == sample).all())

if __name__ == '__main__':

    unittest.main()
