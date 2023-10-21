import gurobipy as gp
from gurobipy import GRB

#change to assume all edges exist
# change to assume "demand" is one array but demand of angels index is q_a

# activation_cost, angel_aid, are provided outside of network

def create_model(nodes_with_depot, nodes, vertices, angels, 
                 edges, edge_weights, activation_cost,
                 demand, angel_demand, angel_aid, communities,
                 vehicle_capacity, max_num_routes) -> gp.Model:
    m = gp.Model()
    x = m.addVars(edges, vtype=GRB.BINARY)
    z = m.addVars(nodes, vtype=GRB.BINARY)
    u = m.addVars(nodes_with_depot)
    u[0].lb = 0
    u[0].ub = 0
    for i in vertices:
        z[i].ub = 0

    cost = 0
    for e in edges:
        cost += edge_weights[e]*x[e]
    for a in angels:
        cost+= activation_cost[a]*z[a]
    m.setObjective(cost, GRB.MINIMIZE)

    # flow balance
    for i in nodes:
        m.addConstr((gp.quicksum(x[e] for e in edges if e[1] == i) 
                    - gp.quicksum(x[e] for e in edges if e[0] == i) 
                    == 0), 
                    f"Flow_Balance_{i}")
        
    # max num routes leaving depot
    m.addConstr((gp.quicksum(x[e] for e in edges if e[0] == 0) <= max_num_routes),
                "Routes_leaving_depot")

    # MTZ multi-route
    for (i,j) in edges:
        if j != 0:
            m.addConstr((u[j] - u[i]
                            >= demand[j] 
                            - gp.quicksum(angel_aid[a]*z[a] for a in angels if j in communities[a])
                            + angel_demand[j]*z[j] - vehicle_capacity*(1-x[(i,j)])),
                            f"MTZ_{i}->{j}")
        
    # bounds on u vars
    for i in nodes:
        m.addConstr((u[i] >= demand[i] + angel_demand[i]*z[i]), f"Uvar_lower_bound_{i}")
        m.addConstr((u[i] <= vehicle_capacity), f"Uvar_upper_bound_{i}")

    return m