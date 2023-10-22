import gurobipy as gp
from gurobipy import GRB
from network import Network
from itertools import combinations_with_replacement

def create_model(nodes_with_depot: list[int], nodes: list[int], vertices: list[int], angels: list[int], 
                 edge_weights: list[list[float]], activation_cost: list[int],
                 demand: list[int], angel_demand: list[int], angel_aid: list[int], communities: list[list[int]],
                 vehicle_capacity: int, max_num_routes: int) -> gp.Model:
    
    edges = [e for e in [(i,j) for i in nodes_with_depot for j in nodes_with_depot] if e[0] != e[1]]
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
        cost += edge_weights[i][j]*x[(i,j)]
    for a in angels:
        cost+= activation_cost[a]*z[a]
    m.setObjective(cost, GRB.MINIMIZE)

    # flow balance
    for n in nodes:
        m.addConstr((gp.quicksum(x[(i,j)] for (i,j) in edges if j == n) # flow in
                    - gp.quicksum(x[(i,j)] for (i,j) in edges if i == n) # flow out
                    == 0), 
                    f"Flow_Balance_{n}")
        
    # max num routes leaving depot
    m.addConstr((gp.quicksum(x[(i,j)] for (i,j) in edges if i == 0) <= max_num_routes),
                "Routes_leaving_depot_max")
    
    # without this constraint, we get trivial solution
    # force at least one route
    m.addConstr((gp.quicksum(x[(i,j)] for (i,j) in edges if i == 0) >= 1),
                "Routes_leaving_depot_min")

    # MTZ multi-route
    for (i,j) in edges:
        if j != 0:
            m.addConstr((u[j] - u[i]
                            >= demand[j] 
                            # - gp.quicksum(angel_aid[a]*z[a] for a in angels if j in communities[a])
                            # + angel_demand[j]*z[j] 
                            - vehicle_capacity*(1-x[(i,j)])),
                            f"MTZ_{i}->{j}")
        
    # bounds on u vars
    for i in nodes:
        m.addConstr(
                    # (
                    u[i] >= demand[i]
                    #  + angel_demand[i]*z[i]), 
                    , f"Uvar_lower_bound_{i}")
        m.addConstr((u[i] <= vehicle_capacity), f"Uvar_upper_bound_{i}")

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