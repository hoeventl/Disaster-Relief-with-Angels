import sys
from network import *
from examples import *
from model import *
from plot import *

network = simple() # create the python data structure holding all the necessary information
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
draw_with_model(network, model)