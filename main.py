# placeholder file for now
from network import *
from experiment import *
from model import *
import sys

# n = Network("Instances/A-n32-k5.vrp", num_angels=1, radius="max")
# m = create_model_from_network(n)
m = create_model_from_network(one_for_all())
m.optimize()
with open("output.txt", "w") as sys.stdout:
    m.display()
sys.stdout = sys.__stdout__

for v in m.getVars():
    if v.X > 0.5:
        print(f"{v.VarName} = {v.X}")