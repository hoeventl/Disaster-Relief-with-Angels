from network import Network

def one_for_all() -> Network:
    """
    Creates a network which has exactly one angel with maximum radius (covers all vertices) and 
    has aid equal to the vertex with the largest demand (satisfies all vertices)
    solution should be route directly to the angel and back, nowhere else.
    """
    # currently will make one angel in a random shadow location but covers all nodes
    n = Network("Instances/A-n32-k5.vrp", num_angels=1, radius="max", aid="max")
    return n

def one_per_cluster() -> Network:
    """
    Creates a network which has one angel per cluster of nodes. Original graph has distinct areas
    for vertices.
    """
    locs = [3,19,25,31] # list of nodes to create an angel under
    n = Network("Instances/B-n31-k5.vrp", num_angels=len(locs), angel_locs=locs, radius=15, aid="max")
    return n

def one_under_each() -> Network:
    """
    Creates a network which has an angel directly under each vertex. Each angel can satisfy all 
    demands. Each angel has a non-trivial radius (community). This recovers the TSP-cover problem.
    """
    n = Network("Instances/A-n32-k5.vrp", num_angels="max", radius=20, aid="max")
    n.demand = [1 if d > 0 else 0 for d in n.demand]
    n.angel_demand = [1 if d > 0 else 0 for d in n.angel_demand]
    n.angel_aid = [1 if a > 0 else 0 for a in n.angel_aid]
    n.activation_cost = [1 if c > 0 else 0 for c in n.activation_cost]
    n.vehicle_capacity = 100
    n.max_num_routes = 1
    return n

def simple() -> Network:
    """
    Creates a simple example of vehicle routing with 3 angels in place.
    """
    n = Network("Instances/X-n11-k25.vrp", num_angels=3, radius=100)
    n.demand = [5 if d > 0 else 0 for d in n.demand]
    n.angel_demand = [8 if d > 0 else 0 for d in n.angel_demand]
    n.angel_aid = [5 if a > 0 else 0 for a in n.angel_aid]
    n.activation_cost = [1 if c > 0 else 0 for c in n.activation_cost]
    n.vehicle_capacity = 16
    n.max_num_routes = 7
    return n

def regular_vrp() -> Network:
    """
    Creates a regular vehicle routing problem without angels. This is primarliy used for 
    verification that the model formulation is valid for the reduced problem.
    """
    n = Network("Instances/A-n32-k5.vrp", num_angels=0)
    return n