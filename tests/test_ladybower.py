""" Lady Bower tests """
import unittest
from unittest.mock import Mock

import collections

from everest import ladybower

class TestWeightedReservoit(unittest.TestCase):

    def test_isample_without_replacement(self):
        """ Call the method

        Will fail if random number generator changes.
        """
        data = [(x + 1, x) for x in range(100)]

        res = ladybower.WeightedReservoir(data, seed=0)

        counter = collections.Counter()
        
        sample = res.isample_without_replacement(10)

        expect = [70, 68, 20, 38, 66, 72, 52, 89, 98, 27]
        self.assertTrue((expect == sample).all())

    def test_isample_all_without_replacement(self):
        """ Sample size is same as reservoir size

        Should return all values """

        size = 20
        data = [(x + 1, x) for x in range(size)]

        res = ladybower.WeightedReservoir(data, seed=1)

        counter = collections.Counter()
        
        sample = res.isample_without_replacement(size)

        expect = set(range(size))
        observe = set(x for x in sample)
        self.assertTrue(expect == observe)


    def test_invalid_input(self):
        """ Exception thrown if invalid parameters """
        size = 10
        data = [(x + 1, x) for x in range(size)]

        res = ladybower.WeightedReservoir(data, seed=1)

        with self.assertRaises(ValueError) as cm:
            sample = res.isample_without_replacement(size + 1)
            
        self.assertEqual(cm.exception.args[0], "Sample size should be <= 10")
        

if __name__ == '__main__':

    unittest.main()
 
