import sys
from network import *
from experiment import *
from model import *
from plot import *

network = one_per_cluster() # create the python data structure holding all the necessary information
model = create_model_from_network(network) # create a Gurobi model from the network
model.optimize()

# print final model to alternative text file
with open("output.txt", "w") as sys.stdout:
    model.display()
sys.stdout = sys.__stdout__

# print solution to console
for v in model.getVars():
    if v.X > 0.5:
        print(f"{v.VarName} = {v.X}")

# generate a graph showing solution
draw(network, model)