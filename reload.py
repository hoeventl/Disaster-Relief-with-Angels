from model import *
from plot import *

for r in range(45,150,10):
    network_path = f"output/radius/network_r-{r}.pickle"
    sol_path = f"output/radius/sol_r-{r}.json"
    network = pickle.load(open(network_path, "rb"))
    sol = json.load(open(sol_path, "rb"))
    draw(network_path, sol_path)

    # next to do, analyze the solution via different metrics, likely will need the model and solution objects
    # and therefore want to change draw to use the objects and not do anything with loading
    # Currently not very clean code...lol