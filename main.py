from network import *
from experiment import *
from model import *
import sys

n = Network("Instances/X-n11-k25.vrp", num_angels=3)
m = create_model_from_network(n)
# m = create_model_from_network(one_for_all())
# m = create_model_from_network(one_per_cluster())
# m = create_model_from_network(one_under_each())
m.optimize()
with open("output.txt", "w") as sys.stdout:
    m.display()
sys.stdout = sys.__stdout__

for v in m.getVars():
    if v.X > 0.5:
        print(f"{v.VarName} = {v.X}")