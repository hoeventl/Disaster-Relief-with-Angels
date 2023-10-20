import vrplib
from parse_distance import pairwise_euclidean
from numpy.random import randint, random_integers
import numpy as np

class Network:

    def __init__(self) -> None:
        self._instance = {}
        pass

    def load_vrp(self):
        self._instance = vrplib.read_instance("Instances/X-n101-k25.vrp")

    # Adds a random 10 angels with random demand to the instance
    # now assumes that "demand" is same array for vertices and angels
    # the angels will always be the last X nodes in the list
    # very dependent on the index now...
    def add_angels_to_instance(self):
        num_angels = 10
        idx = np.sort(randint(1, self._instance['node_coord'].shape[0], num_angels))
        self._instance['node_coord'].append(self._instance['node_coord'][idx])
        max_demand = np.amax(self._instance['demand'])
        self._instance['demand'].append(random_integers(0,max_demand, size=num_angels))
        self._instance['edge_weight'] = pairwise_euclidean(self._instance['node_coord'])
