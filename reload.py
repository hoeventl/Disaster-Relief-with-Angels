from model import *
from plot import *

for r in range(45,150,10):
    network_path = f"output/radius/network_r-{r}.pickle"
    sol_path = f"output/radius/sol_r-{r}.json"
    draw(network_path, sol_path)