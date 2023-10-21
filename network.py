from vrplib.parse_distance import pairwise_euclidean
from vrplib.read_instance import read_instance
from numpy.random import choice, random_integers, default_rng
import numpy as np

class Network:

    def __init__(self) -> None:
        self._instance = {}
        self._rng = default_rng()
        pass

    def load_vrp(self, path):
        self._instance = read_instance(path)

    # Adds a random 10 angels with random demand to the instance
    # now assumes that "demand" is same array for vertices and angels
    # the angels will always be the last X nodes in the list
    # very dependent on the index now...
    def add_angels_to_instance(self, num_angels: int, radius: float):
        # radius to determine community effect, 0 means help its shadow only
        # idx = np.sort(choice(range(1,self._instance['node_coord'].shape[0]), num_angels))
        angels = self._rng.choice(self._instance['node_coord'], num_angels, replace=False)
        print(self._instance['node_coord'])
        print(angels)
        self._instance['node_coord'] = np.concatenate((self._instance['node_coord'], angels))
        print(self._instance['node_coord'])
        max_demand = np.amax(self._instance['demand'])
        self._instance['demand'] = np.concatenate((self._instance['demand'], 
                                             self._rng.integers(0, max_demand, size=num_angels)))
        self._instance['edge_weight'] = pairwise_euclidean(self._instance['node_coord'])
        self._instance['community'] = self._instance['edge_weight'][-num_angels:] <= radius


n = Network()
n.load_vrp("Instances/X-n11-k25.vrp")
n.add_angels_to_instance(4,100)
print(n._instance)