import pickle
import gurobipy as gp
from model import *
from plot import *

network_path = "output/radius/network_r-75.pickle"
sol_path = "output/radius/sol_r-75.json"
# f = open("output/radius/network_r-75.pickle", "rb")
# network = pickle.load(f)
# m = gp.read("output/radius/model_r-75.mps")
# m.read("output/radius/sol_r-75.json")
# m.optimize()

# need to create my own method to load the solution file, will likely use json files instead? sol file is easy to interpret
# m.optimize()

draw(network_path, sol_path)