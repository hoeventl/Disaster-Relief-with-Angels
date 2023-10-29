from vrplib.parse_distance import pairwise_euclidean
from vrplib.read_instance import read_instance
from numpy.random import default_rng
import numpy as np
from re import search

class Network:

    def __init__(self, path: str, num_angels: int = None, radius: float = None, aid: int = None,
                 max_num_routes: int = None) -> None:
        self._instance = read_instance(path)
        self._rng = default_rng()
        self._num_angels, self._radius = self.get_angel_parameters(num_angels, radius)
        self._add_angels_to_instance()
        if max_num_routes is None:
            self.max_num_routes = int(search("-k(.*).vrp", path).group(1)) # https://stackoverflow.com/a/3369000
        else:
            self.max_num_routes = max_num_routes

        # These are sets of indices
        self.nodes_with_depot = self.get_nodes_with_depot()
        self.nodes = self.nodes_with_depot[1:]
        self.vertices = self.nodes[:-self._num_angels] if num_angels != 0 else self.nodes
        self.angels = self.nodes_with_depot[-self._num_angels:] if num_angels != 0 else []
        self.communities = self.get_communities()

        # These are values
        self.edge_weights = self._instance['edge_weight'].tolist()
        self.demand = self._instance['demand'].tolist()
        self.angel_demand = self._instance['angel_demand'].tolist()
        self.vehicle_capacity = self._instance['capacity']

        # Arbitrarily determined
        self.activation_cost = np.concatenate(
            (np.zeros(len(self.nodes_with_depot) - self._num_angels), 
             self._num_angels*self._rng.random(self._num_angels)
             )).tolist() if num_angels != 0 else []
        self.angel_aid = np.concatenate(
            (np.zeros(len(self.nodes_with_depot) - self._num_angels),
            #  self._rng.integers(1, self.vehicle_capacity, self._num_angels)
            np.full(self._num_angels, np.amax(self._instance['demand'])) # force max aid possible for now
             )).tolist() if num_angels != 0 else []

    def get_angel_parameters(self, num_angels: int = None, radius: float = None):
        if num_angels is None:
            num_angels = self._rng.integers(1,self._instance['node_coord'].shape[0]/3)
        if radius is None:
            if num_angels == 0:
                radius = 0
            else:
                radius = self._rng.random()*np.amax(self._instance['edge_weight'])/3
        elif radius == "max":
            radius = np.amax(self._instance['edge_weight'])
        return num_angels, radius

    # Adds a random number angels with random demand to the instance
    # now assumes that "demand" is same array for vertices and angels
    # the angels will always be the last X nodes in the list
    # very dependent on the index now...
    def _add_angels_to_instance(self) -> None:
        angels = self._rng.choice(self._instance['node_coord'], self._num_angels, replace=False)
        self._instance['node_coord'] = np.concatenate((self._instance['node_coord'], angels))
        max_demand = np.amax(self._instance['demand'])
        angel_demand = self._rng.integers(0, max_demand, size=self._num_angels)
        self._instance['angel_demand'] = np.concatenate(
            (np.zeros_like(self._instance['demand']), angel_demand))
        self._instance['demand'] = np.concatenate(
            (self._instance['demand'], np.zeros_like(angel_demand)))
        self._instance['edge_weight'] = pairwise_euclidean(self._instance['node_coord'])
        vertex_community = np.full(
            self._instance['edge_weight'][:-self._num_angels].shape, 
            False) # top part of array
        angel_to_vertex_community = self._instance['edge_weight'][-self._num_angels:,:-self._num_angels] \
                                        <= self._radius # bottom left of array
        angel_to_angel_community = np.full(
            self._instance['edge_weight'][-self._num_angels:,-self._num_angels:].shape,
            False) # bottom right of array
        angel_community = np.concatenate(
            (angel_to_vertex_community, 
             angel_to_angel_community),
             axis=1) # bottom part of array
        self._instance['community'] = np.concatenate((vertex_community, angel_community))

    # Gets a set of indices which are the ground set of all nodes in the network including angels
    def get_nodes_with_depot(self) -> list:
        return list(range(self._instance['node_coord'].shape[0]))

    # gets a complete 2d array of "adjacency-like" communities
    # e.g. [[], [], [], [1,3], [2,4]]
    # where the angels are the tail of the list
    def get_communities(self) -> list[list[int]]:
        communities = []
        for i in range(self._instance['community'].shape[0]):
            community = []
            for j in range(self._instance['community'].shape[1]):
                if self._instance['community'][i][j]:
                    community.append(j)
            communities.append(community)
        return communities
    