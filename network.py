from vrplib.parse_distance import pairwise_euclidean
from vrplib.read_instance import read_instance
from numpy.random import default_rng
import numpy as np
from re import search

class Network:

    def __init__(self, 
                 path: str, 
                 num_angels: int = None, 
                 radius: float | str | list = None, 
                 aid: int | str = None,
                 max_num_routes: int = None, 
                 angel_locs: list = None, 
                 angel_demand: int | list = None,
                 activation_cost = int | list | None) -> None:
        """
        Please make sure that you provide num_angels if locs or aid is provided as an explicit list
        """
        self._instance = read_instance(path)
        self._instance_file = path
        self._rng = default_rng()
        self._num_angels, self._radius = self._set_angel_parameters(num_angels, radius)
        self._add_angels_to_instance(angel_locs, angel_demand)
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
        self.angel_aid = self.set_angel_aid(aid)

        # Arbitrarily determined
        self.activation_cost = self.set_angel_activation_cost(activation_cost) # probably does not need to be detemined here but in model

    # def _check_angel_sizes(self, aid, locs) -> bool | int:
    #     if aid is None and isinstance(locs,list):
    #         return len(locs)
    #     if locs is None and aid is not None:
    #         return len(aid)
    #     if isinstance(aid,list) and isinstance(locs,list):
    #         num_angels = len(aid)
    #         if num_angels == len(locs): 
    #             return num_angels
    #     return False

    def _set_angel_parameters(self, num_angels: int | None, radius: float | str | list | None):
        if num_angels is None:
            num_angels = self._rng.integers(1,self._instance['node_coord'].shape[0]/3)
        elif num_angels == "max":
            num_angels = self._instance['node_coord'].shape[0] - 1 # exclude depot
        if radius is None:
            if num_angels == 0:
                radius = [0]
            else:
                radius = [self._rng.random()*np.amax(self._instance['edge_weight'])/3 \
                          for _ in range(num_angels)]
        elif radius == "max":
            radius = [np.amax(self._instance['edge_weight']) \
                      for _ in range(num_angels)]
        elif isinstance(radius, list):
            radius = radius
        elif isinstance(radius, int):
            radius = [radius for _ in range(num_angels)]
        return num_angels, radius
    
    def set_angel_aid(self, aid: int | str | None) -> list[int]:
        vertex_aid = np.zeros(len(self.nodes_with_depot) - self._num_angels)
        if aid is None:
            angel_aid = np.concatenate(
            (vertex_aid,
             self._rng.integers(1, np.amax(self._instance['demand']), self._num_angels)
             )).tolist()
        elif aid == "max":
            angel_aid = np.concatenate(
                (vertex_aid,
                np.full(self._num_angels, np.amax(self._instance['demand']))
                )).tolist()
        elif aid > 0:
             angel_aid = np.concatenate((vertex_aid, np.full(self._num_angels, aid))).tolist()
        else:
            angel_aid = []
        return angel_aid
    
    def set_angel_activation_cost(self, cost: int | list | None) -> list:
        # overkill for this parameter
        if self._num_angels == 0:
            return []
        vertex_activation_costs = np.zeros(len(self.nodes_with_depot) - self._num_angels)
        angel_activation_costs = np.zeros(self._num_angels)
        if cost is None:
            angel_activation_costs = self._rng.random(self._num_angels) \
                                        * np.amax(self._instance['node_coord']) \
                                        + 1
        elif isinstance(cost, int):
            angel_activation_costs = np.full(self._num_angels, cost)
        elif isinstance(cost, list):
            angel_activation_costs = np.asarray(cost)
        return np.concatenate((vertex_activation_costs, angel_activation_costs)).tolist()

    def _add_angels_to_nodes(self, locs: list | None) -> None:
        if locs is None:
            angels = self._rng.choice(self._instance['node_coord'][1:], self._num_angels, replace=False)
        elif isinstance(locs[0], tuple):
            angels = locs
        elif isinstance(locs[0], int):
            angels = self._instance['node_coord'][[i-1 for i in locs]]
        self._instance['node_coord'] = np.concatenate((self._instance['node_coord'], angels))

    def _add_angel_demand(self, demand: int | list | None) -> None:
        max_demand = np.amax(self._instance['demand'])
        if demand is None:
            angel_demand = self._rng.integers(1, max_demand, size=self._num_angels)
        elif isinstance(demand, int):
            angel_demand = np.full(self._num_angels, demand)
        elif isinstance(demand, list):
            angel_demand = np.asarray(demand)

        self._instance['angel_demand'] = np.concatenate(
            (np.zeros_like(self._instance['demand']), angel_demand))
        self._instance['demand'] = np.concatenate(
            (self._instance['demand'], np.zeros_like(angel_demand)))

    def _update_edge_weights(self) -> None:
        self._instance['edge_weight'] = pairwise_euclidean(self._instance['node_coord'])

    def _create_angel_communities(self) -> None:
        vertex_to_vertex_community = np.full(
            self._instance['edge_weight'][:-self._num_angels].shape, 
            False) # top part of array
        angel_to_vertex_community = np.zeros_like(\
            self._instance['edge_weight'][-self._num_angels:,:-self._num_angels]) # bottom left of array
        for a in range(self._num_angels):
            community = self._instance['edge_weight'][-self._num_angels+a,:-self._num_angels] \
                <= self._radius[a]
            angel_to_vertex_community[a] = community
        angel_to_angel_community = np.full(
            self._instance['edge_weight'][-self._num_angels:,-self._num_angels:].shape,
            False) # bottom right of array
        angel_community = np.concatenate(
            (angel_to_vertex_community, 
             angel_to_angel_community),
             axis=1) # bottom part of array
        self._instance['community'] = np.concatenate((vertex_to_vertex_community, angel_community))

    # Adds a random number angels with random demand to the instance
    def _add_angels_to_instance(self, locs: list | None, angel_demand: int | list | None) -> None:
        self._add_angels_to_nodes(locs)
        self._add_angel_demand(angel_demand)
        self._update_edge_weights()
        self._create_angel_communities()

    # Gets a set of indices which are the ground set of all nodes in the network including angels
    def get_nodes_with_depot(self) -> list:
        return list(range(self._instance['node_coord'].shape[0]))

    # gets a complete 2d array of "adjacency-like" communities
    # e.g. [[], [], [], [1,3], [2,4]]
    # where the angels are the tail of the list
    def get_communities(self) -> list[list[int]]:
        """
        Creates a 2D (n+m by ?) list of indices which serves as an "adjacency" matrix. 
        Each sublist is a set of vertices which are within the radius of the node.
        The first axis corresponds to each node, excluding the depot, starting with the vertices and
        the tail corresponds to the angels.
        e.g. [[], [], [], [1,3], [2,4]]
        """
        communities = []
        for i in range(self._instance['community'].shape[0]):
            community = []
            for j in range(self._instance['community'].shape[1]):
                if self._instance['community'][i][j]:
                    community.append(j)
            communities.append(community)
        return communities
    
    def get_coordinates(self) -> dict:
        """
        Returns a dictionary of the nodes in the graph [vertices, angels] where the key is the index
        and the value is the Euclidean coordinates taken from the instance.
        """
        return {k:v for k,v in enumerate(self._instance['node_coord'].tolist())}
    