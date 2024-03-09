import os, pickle, json
from network import *
from model import *
from plot import *

def variable_radius(instance: str, folder_destination: str, suffix: str, values: list[int]):
    for r in values:
        network = Network(instance,\
                          num_angels=1,\
                          radius=r,\
                          angel_locs=[(250,250)],\
                          aid="max",\
                          angel_demand=20,\
                          activation_cost=20)
        model = create_model_from_network(network)
        model.optimize()

        # write solution and model to be loaded and used another day
        mps_path = os.path.join(folder_destination, f"model_{suffix}{r}.mps")
        model.write(mps_path)
        sol_path = os.path.join(folder_destination, f"sol_{suffix}{r}.json")
        model.write(sol_path)
        network_path = os.path.join(folder_destination, f"network_{suffix}{r}.pickle")
        with open(network_path, "wb") as network_file:
            pickle.dump(network, network_file)

def visualize_experiments(folder: str, suffix: str, values: list[int]):
    if not os.path.exists(folder):
        raise Exception(f"Invalid folder path: {folder}")
    
    for x in values:
        network_path = os.path.join(folder, f"network_{suffix}{x}.pickle")
        sol_path = os.path.join(folder, f"sol_{suffix}{x}.json")
        network = pickle.load(open(network_path, "rb"))
        sol = json.load(open(sol_path, "rb"))
        draw(network, sol)


INSTANCE = "./Instances/TH-n11-k2.vrp"
OUTPUT_FOLDER = "./output/"
SUBFOLDER = "radius/"
suffix = "r-"
radius_vals = [0, 40, 70, 85, 100, 125]

# variable_radius(INSTANCE, OUTPUT_FOLDER + SUBFOLDER, suffix, radius_vals)
visualize_experiments(OUTPUT_FOLDER+SUBFOLDER, suffix, radius_vals)