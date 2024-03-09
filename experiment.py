import os, pickle
from network import *
from model import *

INSTANCE = "./Instances/TH-n11-k2.vrp"
OUTPUT_FOLDER = "./output/"
SUBFOLDER = "radius/"

for r in range(45,150,10):
    network = Network(INSTANCE,num_angels=1,radius=r,angel_locs=[(250,250)],aid="max",angel_demand=20,activation_cost=20)
    model = create_model_from_network(network)
    model.optimize()

    # write solution and model to be loaded and used another day
    mps_path = os.path.join(OUTPUT_FOLDER, SUBFOLDER, f"model_r-{r}.mps")
    model.write(mps_path)
    sol_path = os.path.join(OUTPUT_FOLDER, SUBFOLDER, f"sol_r-{r}.json")
    model.write(sol_path)
    network_path = os.path.join(OUTPUT_FOLDER, SUBFOLDER, f"network_r-{r}.pickle")
    with open(network_path, "wb") as network_file:
        pickle.dump(network, network_file)



# generate a graph showing solution
# draw(network, model)