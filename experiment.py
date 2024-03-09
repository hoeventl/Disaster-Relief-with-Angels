import os, pickle, json, glob
from re import search
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
        run_experiment(folder_destination, suffix, r, network)

def variable_angel_demand(instance: str, folder_destination: str, suffix: str, values: list[int]):
    for ad in values:
        network = Network(instance,\
                          num_angels=1,\
                          radius=90,\
                          angel_locs=[(250,250)],\
                          aid="max",\
                          angel_demand=ad,\
                          activation_cost=20)
        run_experiment(folder_destination, suffix, network, ad)

def run_experiment(folder_destination, suffix, network, val):
    model = create_model_from_network(network)
    model.optimize()

        # write solution and model to be loaded and used another day
    mps_path = os.path.join(folder_destination, f"model_{suffix}{val}.mps")
    model.write(mps_path)
    sol_path = os.path.join(folder_destination, f"sol_{suffix}{val}.json")
    model.write(sol_path)
    network_path = os.path.join(folder_destination, f"network_{suffix}{val}.pickle")
    with open(network_path, "wb") as network_file:
        pickle.dump(network, network_file)

def analyze_solutions(folder: str):
    sol_path_style = os.path.join(folder, "sol_*.json")
    sol_paths = glob.glob(sol_path_style)
    network_path_style = os.path.join(folder, "network_*.pickle")
    network_paths = glob.glob(network_path_style)

    if len(sol_paths) != len(network_paths):
        raise Exception("Unable to analyze solutions: inequal amount of network object files and solution files.")

    for i in range(len(sol_paths)):
        suffix = search("sol_(.+?).json", sol_paths[i]).group(1)
        sol = json.load(open(sol_paths[i], "rb"))
        network = pickle.load(open(network_paths[i], "rb"))

        data = {}
        data["instance"] = network._instance_file
        data["experiment"] = suffix
        # do some analysis here based on the solution and network
        active_edges, active_angels = get_active_edges_and_angels(sol)
        # angels = network.nodes[-network._num_angels:]
        # inactive_angels = [a for a in angels if a not in active_angels]
        data["percent_active_angels"] = len(active_angels)/float(network._num_angels)

        communities = network.get_communities()
        angel_aid = network.angel_aid
        demand_covered_by_angels = sum(len(communities[a]) * angel_aid[a] for a in active_angels)
        total_demand_of_network = sum(network.demand)
        data["percent_demand_handled_by_active_angels"] = demand_covered_by_angels/float(total_demand_of_network)

        # write analysis to file
        with open(os.path.join(folder, f"analysis_{suffix}.json"), "w+") as a:
            json.dump(data, a)

def get_active_edges_and_angels(sol: dict):
    active_edges = []
    active_angels = []
    for v in sol["Vars"]:
        if v['X'] > 0.5:
            if v['VarName'].startswith("x"):
                active_edges.append(tuple(eval(v['VarName'][1:])))
            if v['VarName'].startswith("z"):
                active_angels.append(eval(v['VarName'][1:])[0])
    return active_edges, active_angels

def visualize_experiments(folder: str, suffix: str, values: list[int]):
    if not os.path.exists(folder):
        raise Exception(f"Invalid folder path: {folder}")
    
    for x in values:
        network_path = os.path.join(folder, f"network_{suffix}{x}.pickle")
        sol_path = os.path.join(folder, f"sol_{suffix}{x}.json")
        network = pickle.load(open(network_path, "rb"))
        sol = json.load(open(sol_path, "rb"))
        draw(network, sol)

def clear_folder(folder: str):
    files = glob.glob(f"{folder}*")
    for f in files:
        os.remove(f)


INSTANCE = "./Instances/TH-n11-k2.vrp"
OUTPUT_FOLDER = "./output/"
SUBFOLDER = "angel_demand/"
suffix = "ad-"
radius_vals = [0, 60, 70, 95, 105, 125]
angel_demand_vals = [i for i in range(10,51,5)]

# variable_radius(INSTANCE, OUTPUT_FOLDER+SUBFOLDER, suffix, radius_vals)
clear_folder(OUTPUT_FOLDER+SUBFOLDER)
variable_angel_demand(INSTANCE, OUTPUT_FOLDER+SUBFOLDER, suffix, angel_demand_vals)
analyze_solutions(OUTPUT_FOLDER+SUBFOLDER)
# visualize_experiments(OUTPUT_FOLDER+SUBFOLDER, suffix, radius_vals)