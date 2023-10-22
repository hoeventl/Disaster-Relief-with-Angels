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
# num_angels = randint(int(n/2))
num_angels = 0
num_verts = n - 1 - num_angels
max_community_size = min(int(num_verts/num_angels),5) if num_angels !=0 else 0
min_community_size = 1 if num_angels != 0 else 0

# Sets
vertices = sorted(sample(nodes, num_verts))
# will be empty
angels = sorted([k for k in nodes if k not in vertices])
# will be empty
communities = {a: [v for v in sample(vertices, randint(min_community_size, max_community_size))] 
               for a in angels} # completely random communities, not geographically based
edges = [e for e in [(i,j) for i in nodes_with_depot for j in nodes_with_depot] if e[0] != e[1]]

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
print(demand)

m = gp.Model()
x = m.addVars(edges, vtype=GRB.BINARY, name="x")
z = m.addVars(nodes, vtype=GRB.BINARY, name="z")
u = m.addVars(nodes_with_depot, name="u")
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
for n in nodes:
    m.addConstr((gp.quicksum(x[(j,i)] for (j,i) in edges if i == n) # flow in
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
                        - gp.quicksum(angel_aid[a]*z[a] for a in angels if j in communities[a])
                        + angel_demand[j]*z[j] - vehicle_capacity*(1-x[(i,j)])),
                        f"MTZ_{i}->{j}")
    
# bounds on u vars
for i in nodes:
    m.addConstr((u[i] >= demand[i] + angel_demand[i]*z[i]), f"Uvar_lower_bound_{i}")
    m.addConstr((u[i] <= vehicle_capacity), f"Uvar_upper_bound_{i}")

m.optimize()

for v in m.getVars():
    if v.X > 0.5:
        print(f"{v.VarName} = {v.X}")