import sys
from network import *
from experiment import *
from model import *
from plot import *

n = one_per_cluster()
m = create_model_from_network(n)
m.optimize()
with open("output.txt", "w") as sys.stdout:
    m.display()
sys.stdout = sys.__stdout__

for v in m.getVars():
    if v.X > 0.5:
        print(f"{v.VarName} = {v.X}")

draw(n,m)