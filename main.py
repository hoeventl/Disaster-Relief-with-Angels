# placeholder file for now
from network import *
from model import *

n = Network("Instances/X-n101-k25.vrp", num_angels=0, max_num_routes=26)
m = create_model_from_network(n)
m.optimize()

for v in m.getVars():
    if v.X > 0.5:
        print(f"{v.VarName} = {v.X}")