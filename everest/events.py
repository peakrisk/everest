"""
================

Event Generation
================

Starting at the top, with event generation, everest seems like the
obvious choice.

Trivia
======

So Everest is the highest, at least above sea level.  As far as I am
aware there is no danger of it losing that title any time soon.  Maybe
an asteroid hit might have something to say about it.

But there other mountains that can claim the record of the hightest.

The earth bulges along the equator, so the closer you are to the
equator, the further sea level is from the centre of the earth.

The summit of Chimborazo in Ecuador is the furthest point on earth from
the centre. It is just 1 degree south of the equator.  From wikipedia:

     The summit of Mount Everest reaches a higher elevation above sea
     level, but the summit of Chimborazo is widely reported to be the
     farthest point on the surface from Earth's center, with
     Huascarán a very close second. The summit of the Chimborazo is
     the fixed point on Earth which has the utmost distance from the
     center – because of the oblate spheroid shape of the planet Earth
     which is "thicker" around the Equator than measured around the
     poles.  Chimborazo is one degree south of the Equator and
     the Earth's diameter at the Equator is greater than at the
     latitude of Everest (8,848 m (29,029 ft) above sea level), nearly
     27.6° north, with sea level also elevated. Despite being 2,580 m
     (8,465 ft) lower in elevation above sea level, it is 6,384.4 km
     (3,967.1 mi) from the Earth's center, 2,168 m (7,113 ft) farther
     than the summit of Everest (6,382.3 km (3,965.8 mi) from the
     Earth's center).[note 4] However, by the criterion of elevation
     above sea level, Chimborazo is not even the highest peak of the
     Andes.

And then there is the question, which mountain on earth has the
longest climb.  You could argue the answer is Chimborazo.  Start at
the point under the ocean that is closest to the centre of the earth
and work your way to the summit.

Mount Lamlam (meaning lightning in Chamoru) is a peak on the United
States island of Guam. It is located near the village of Agat (5 km or
3 mi[3] north), in the southwest of the island.

Rising to 406 meters (1,332 ft) above sea level, it is the highest
peak in Guam (before Mount Jumullong Manglo). The distance from the
peak to the bottom of the nearby Mariana Trench is the greatest change
in elevation on Earth over such a short distance.

So, if you go to Guam and make the modest 1300 foot climb you can
arguably claim to be on the tallest mountain on earth.


LICENSE
=======

FIXME: add a license file
GPL v 3
"""
import os
import json
from collections import defaultdict

import pandas as pd
import numpy as np

import networkx as nx

from everest import utils

class Everest(object):
    """ A mountain of events

    The events come from separate hills, or EventGenerators.
    """
    def __init__(self):
        """ Initialise Everest """
        self.hills = defaultdict(list)
        
    def load(self, data):
        """ Load a model

        Data is a list of dictionaries.

        Each dictionary describes a part of the model.
        """
        for item in data:

            # class is implementation for this event generator
            clazz = utils.get_class(item.get(
                'class', 'everest.events.EventGenerator'))

            hill = clazz(item)

            self.hills[hill.short_name()].append(hill)

        self.build_graph()

    def dump(self):
        """ Dump out current model """
        print(self.hills)


    def build_graph(self):
        """Build graph of relationships between hills 

        Each hill is a list of things that can be used for that hill.

        Each of these may have inputs (names of other hills).

        A graph is build to show the input relations.

        Checks in case graph is cyclic.

        Does a topological sort on the hills to give and order in
        which they should be processed.
        """
        graph = nx.DiGraph()

        for hill, data in self.hills.items():

            for item in data:
                for link in item.inputs:
                    graph.add_edge(link, hill)

        # check if graph is acyclic
        is_dag = nx.is_directed_acyclic_graph(graph)

        if not is_dag:
            raise ValueError("hills must be acyclic")

        self.hill_order = nx.topological_sort(
            graph)


    def seed(self, seed):
        """ Seed random number generators """
        self.random = np.random.RandomState(seed)

        for hill, choice, ix in self.walk_hills():
            # include the hill and choice index in the seed
            # to avoid identical seeding for different hills.
            full_seed = [seed, ix] + [ord(x) for x in ''.join(hill)]
            choice.seed(full_seed)

    def initialise(self):
        """ Initialise all the hills """
        for hill, choice, ix in self.walk_hills():
            choice.initialise()

    def walk_hills(self):
        """ Walk through all the hills """
        for hill, choices in self.hills.items():
            for ix, choice in enumerate(choices):
                yield (hill, choice, ix)

    def generate_trials(self, start=0, end=1000,
                        start_time=None, end_time=None):
        """ Generate trials of events.

        Each trial covers a period from start_time to end_time.

        Trials will be numbered from start to end-1.

        Seeding of random number generators will be such that the same
        results will be returned given the same input parameters.

        start: datetime object, default datetime.datetime.now()

        end: datetime object, defauilt datetime.datetime.now + 1 year  
        """
        for trial in range(start, end):
            yield self.generate_trial(
                start_time, end_time)


    def generate_trial(self,
                       start_time=None, end_time=None):
        """ Generate a single trial """

        events = {}
        for hill in self.hill_order:
            # pick a hill
            choices = self.hills[hill]
            if not choices:
                continue
            
            which = self.random.randint(len(choices))

            choice = choices[which]
            hill_events = [x for x in
                           choice.generate_trial(
                               start_time, end_time,
                               events)]
            events[hill] = dict(
                events=hill_events,
                name=choice.full_name())

        return events


class EventGenerator(object):

    def __init__(self, parms=None):

        self.inputs = []
        if parms:
            self.__dict__.update(parms)

        # Set up random state
        self.random = np.random.RandomState()
            
    def seed(self, seed):
        """ Seed the random number generator """
        self.random.seed(seed)

    def initialise(self):
        """ Do stuff like loading pools of events and their frequencies.

        Initialisation should be done after seeding.
        """
        pass

    def generate_trials(self, n=1):
        """ Generate n trials of events 
        
        FIXME: not sure we need this method.
        """
        for trial in range(n):
            yield self.generate_trial()

    def number_of_events(self,
                         start_time=None,
                         end_time=None,
                         events=None):

        return 0

    def generate_trial(self,
                       start_time=None,
                       end_time=None,
                       events=None):
        """  Return a single trial of events """
        # Get number of events
        n = self.number_of_events(
            start_time, end_time,
            events)

        for event in range(n):
            yield self.pick_event()

    def pick_event(self):
        """ Pick an event """
        return Event()

    def inputs(self):
        """ Return the inputs that this event generator needs """
        return self.parms.get('inputs')

    def short_name(self):
        """ Return short name for this generator. """
        return '_'.join((self.region, self.peril))

    def full_name(self):
        """ Return full name for this generator. """
        return '_'.join((self.source, self.region, self.peril,
                         self.version))


class Event(object):
    pass


class Poisson(EventGenerator):

    def number_of_events(self,
                         start_time=None,
                         end_time=None,
                         events=None):
        """ Return the number of events """
        return self.random.poisson(self.frequency)
        

class NegativeBinomial(EventGenerator):

    def number_of_events(self,
                         start_time=None,
                         end_time=None,
                         events=None):
        """ Number of events per trial """
        return self.random.negative_binomial(self.n, self.p)


class WeightedEventSampler(object):
    """ Given n objects with weights w_1, ... 2_n select m of them 

    For example:

    >>> data = {a=1., b=2., c=3.}
    
    >>> sampler = WeightedEventSampler(data)

    >>> sampler.sample(1)
    """
    def __init__(self, data):
        """ """
        self.data = data
        self.total_weight = sum(data[x] for x in data)

    def sample(self, n):

        delta = self.total_weight / n


if __name__ == '__main__':

    import sys

    model = '.'
    if len(sys.argv) > 1:
        model = sys.argv[1]

    everest = Everest()

    data = utils.load_json_from_folder(model)
    everest.load(data)
    everest.seed(0)
    everest.initialise()

    for x in everest.generate_trials(end=10):
        for key, data in x.items():
            print(key, len(data['events']), data['name'])
              
            
