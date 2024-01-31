import sys
from network import *
from experiment import *
from model import *
from plot import *

network = one_per_cluster()
model = create_model_from_network(network)
model.optimize()
with open("output.txt", "w") as sys.stdout:
    model.display()
sys.stdout = sys.__stdout__

for v in model.getVars():
    if v.X > 0.5:
        print(f"{v.VarName} = {v.X}")

draw(network, model)