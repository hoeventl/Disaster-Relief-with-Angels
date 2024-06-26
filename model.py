import gurobipy as gp
from gurobipy import GRB
from network import Network

# need to confirm these dimensions

def create_model(nodes_with_depot: list[int], nodes: list[int], vertices: list[int], angels: list[int], 
                 edge_weights: list[list[float]], activation_cost: list[int],
                 demand: list[int], angel_demand: list[int], angel_aid: list[int], communities: list[list[int]],
                 vehicle_capacity: int, max_num_routes: int) -> gp.Model:
    """ 
    nodes_with_depot = [0,1,2,3,4,...,n+m] (n+m+1 by 1)
    nodes = [*vertices, *angels] = nodes_with_depot[1:] = nodes_with_depot \ {0}
    vertices = [1,2,3,4,...,n-m-1,n-m]
    angels = [n-m+1,n-m+2,...,n+m]
    edge_weights = [[x,x,x,x,x],[x,x,x,x]] ... (n+m+1 by n+m+1)
    activation_cost = [0,0,0,0,0,...,x,x,x,...] nonzero for all angels (n+m by 1)
    communities = [[],[],[],...,[1,2,3], [2,3]] only valid for angels (n+m by 1)
    """
    
    EPSILON = 1e-4 # needed to prevent "self" loops from vertex to angel below and back
    edges = [e for e in [(i,j) \
                         for i in nodes_with_depot \
                            for j in nodes_with_depot if edge_weights[i][j] > 0] \
                    if e[0] != e[1]]
    m = gp.Model()
    x = m.addVars(edges, vtype=GRB.BINARY, name="x")
    z = m.addVars(nodes, vtype=GRB.BINARY, name="z")
    u = m.addVars(nodes_with_depot, name="u")
    u[0].lb = 0
    u[0].ub = 0
    for i in vertices:
        z[i].ub = 0 

    cost = 0
    for (i,j) in edges:
        cost += (edge_weights[i][j]+EPSILON)*x[(i,j)]
    for a in angels:
        cost += activation_cost[a]*z[a]
    m.setObjective(cost, GRB.MINIMIZE)

    # flow balance
    for n in nodes:
        m.addConstr((gp.quicksum(x[(i,j)] for (i,j) in edges if j == n) # flow in
                    - gp.quicksum(x[(i,j)] for (i,j) in edges if i == n) # flow out
                    == 0), 
                    f"Flow_Balance_{n}")
        
        # force flow in to a node if demand exists
        m.addConstr((gp.quicksum(x[(i,j)] for (i,j) in edges if j == n)
                    >= (demand[n] 
                    - gp.quicksum(angel_aid[a]*z[a] for a in angels if n in communities[a])
                    + angel_demand[n]*z[n]
                    ) / float(demand[n] + angel_demand[n])),
                    f"Require_flow_in_{n}")
        
        # bounds on u variables
        m.addConstr((u[n] >= demand[n] + angel_demand[n]*z[n]), 
                    f"Uvar_lower_bound_{n}")
        m.addConstr((u[n] <= vehicle_capacity), f"Uvar_upper_bound_{n}")
        
    
    # MTZ multi-route
    for (i,j) in edges:
        if j != 0: # everything but the depot
            m.addConstr((u[j] - u[i]
                            >= demand[j] 
                            - gp.quicksum(angel_aid[a]*z[a] for a in angels if j in communities[a])
                            + angel_demand[j]*z[j] 
                            - vehicle_capacity*(1-x[(i,j)])),
                            f"MTZ_{i}->{j}")
            # had to add this constraint to force routing starting from depot
            m.addConstr((u[j] - u[i] >= -vehicle_capacity*(1-x[(i,j)])), f"Uvardiff_{i}->{j}")
    
    # max num routes leaving depot
    m.addConstr((gp.quicksum(x[(i,j)] for (i,j) in edges if i == 0) <= max_num_routes),
                "Routes_leaving_depot_max")
        
    return m

def create_model_from_network(n: Network) -> gp.Model:
    return create_model(
        n.nodes_with_depot,
        n.nodes,
        n.vertices,
        n.angels,
        n.edge_weights,
        n.activation_cost,
        n.demand, 
        n.angel_demand, 
        n.angel_aid, 
        n.communities,
        n.vehicle_capacity, 
        n.max_num_routes
    )