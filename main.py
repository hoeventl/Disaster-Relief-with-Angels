# placeholder file for now
from network import *
from model import *

n = Network("Instances/X-n11-k25.vrp", num_angels=0)
m = create_model_from_network(n)
m.optimize()

for v in m.getVars():
    print(f"{v.VarName} = {v.X}")