# placeholder file for now
from network import *
from model import *

n = Network("Instances/X-n101-k25.vrp")
m = create_model_from_network(n)
m.optimize()