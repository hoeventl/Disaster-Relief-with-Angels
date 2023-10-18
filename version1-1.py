#
# Disaster Relief Vehicle Routing Problem (VRP) with Angels
# Thomas Hoevener, Chrysafis Vogiatzis
#

import gurobipy as gp
from gurobipy import GRB
from random import sample, randint, seed
from itertools import combinations_with_replacement
import networkx as nx

seed(1) # fix construction


# Network Generation Parameters
n = 10 + 1
nodes = range(1,n)
nodes_with_depot = range(n)
num_verts = randint(int(n/2), n-2) # make sure at least one angel
num_angels = n - 1 - num_verts
max_community_size = min(int(num_verts/num_angels),5)
min_community_size = 1

# Sets
vertices = sorted(sample(nodes, num_verts))
angels = sorted([k for k in nodes if k not in vertices])
communities = {a: [v for v in sample(vertices, randint(min_community_size, max_community_size))] 
               for a in angels} # completely random communities, not geographically based
tmp = sample(list(combinations_with_replacement(nodes_with_depot, 2)), randint(2*n, int(n*n/2))) 
edges = sorted([e for e in tmp if e[0] != e[1]]) # remove any self loops

print(vertices) # should be [1,2,4,5,6,10] with given seed

# Parameters
edge_weights = {e: randint(1,n) for e in edges} # w_ij
activation_cost = {} # c_a
angel_aid = {} # alpha
demand = {} # d_i
angel_demand = {} # q_a
for i in nodes:
    if i in angels:
        activation_cost[i] = randint(num_angels,n)
        angel_aid[i] = randint(1,10)
        demand[i] = 0
        angel_demand[i] = randint(int(n/2),n)
    else:
        activation_cost[i] = 0
        angel_aid[i] = 0
        demand[i] = randint(1,2)
        angel_demand[i] = 0
max_num_routes = 3 # K
vehicle_capacity = 4 # Q

# could probably have one master set which associates angels and their various sets and weights,
# same for nodes


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

m.optimize()