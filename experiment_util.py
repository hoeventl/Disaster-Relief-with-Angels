import os, pickle, json, glob
import networkx as nx
from re import search
from random import random
from network import *
from model import *
from plot import *

INFINITY = 1e100

def variable_radius(instance: str, folder_destination: str, suffix: str, values: list[int]):
    for r in values:
        network = Network(instance,
                            num_angels=3,
                            radius=r,
                            aid=16,
                            angel_locs=[(45,55), (70,70), (10,10)],
                            angel_demand=40,
                            activation_cost=25)
        experiment_name = f"{suffix}{r}"
        run(folder_destination, network, experiment_name)

def variable_angel_demand(instance: str, folder_destination: str, suffix: str, values: list[int]):
    for ad in values:
        network = Network(instance,
                            num_angels=3,
                            radius=25,
                            aid=16,
                            angel_locs=[(45,55), (70,70), (10,10)],
                            angel_demand=ad,
                            activation_cost=25)
        experiment_name = f"{suffix}{ad}"
        run(folder_destination, network, experiment_name)

def variable_activation_cost(instance: str, folder_destination: str, suffix: str, values: list[int]):
    for w in values:
        network = Network(instance,
                            num_angels=3,
                            radius=25,
                            aid=16,
                            angel_locs=[(45,55), (70,70), (10,10)],
                            angel_demand=40,
                            activation_cost=w)
        experiment_name = f"{suffix}{w}"
        run(folder_destination, network, experiment_name)

def variable_connectivity(instance: str, folder_destination: str, suffix: str, values: list[float], num_trials: int):
    """
    Creates networks where the connectivity of the graph varies according to the values which
    determine the probability that an edge is included in the graph. 
    Example: values = [0.1, 0.3, 0.5, 0.9] -> 10% of edges, 30% of edges, ...
    """
    for p in values:
        for t in range(1, num_trials+1):
            network = Network(instance,
                            num_angels=3,
                            radius=25,
                            aid=16,
                            angel_locs=[(45,55), (70,70), (10,10)],
                            angel_demand=40,
                            activation_cost=25)
            weights = network.edge_weights
            num_nodes = len(weights)
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if random() > p:
                        weights[i][j] = INFINITY
            network.set_edge_weights(weights)
            experiment_name = f"{suffix}{p}({t})"
            run(folder_destination, network, experiment_name)

def run(folder_destination: str, network: Network, experiment_name: str, time_limit: float = 3*60*60):
    """
    folder_destination  : where to place the model, solution, and network files
    network             : a Network object
    experiment_name     : what to call the experiment (should be unique from others in same folder)
    time_limit          : in seconds, the maximum amount of time allowed for solving (default is 3 hours)
    """
    model = create_model_from_network(network)
    if time_limit:
        model.setParam("TimeLimit", time_limit)
    model.optimize()

    if model.Status in [GRB.OPTIMAL, GRB.INTERRUPTED, GRB.TIME_LIMIT]:
        # write the solution if optimal or stopped by user
        sol_path = os.path.join(folder_destination, f"sol_{experiment_name}.json")
        model.write(sol_path)
    elif model.Status == GRB.INFEASIBLE:
        # write IIS (Irreducible Infeasible Subsystem) if failed to solve for any reason
        iis_path = os.path.join(folder_destination, f"iis_{experiment_name}.ilp")
        model.write(iis_path)
    else:
        # failed for some other reason
        with open(os.path.join(folder_destination, f"./failed_{experiment_name}.txt"), "w+") as f:
            f.write("This model failed to solve for reasons other than infeasiblity.")

    # write model and network object to file for later reload
    mps_path = os.path.join(folder_destination, f"model_{experiment_name}.mps")
    model.write(mps_path)
    network_path = os.path.join(folder_destination, f"network_{experiment_name}.pickle")
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
        experiment_name = search("sol_(.+?).json", sol_paths[i]).group(1)
        sol = json.load(open(sol_paths[i], "rb"))
        network = pickle.load(open(network_paths[i], "rb"))

        # do some analysis here based on the solution and network
        data = {}
        data["instance"] = network._instance_file
        data["experiment"] = experiment_name
        active_edges, active_angels = get_active_edges_and_angels(sol)
        data["angel_data"] = create_angel_data(network, active_angels)
        data["graph_data"] = create_graph_data(sol, network)
        data["network_data"] = network.to_dict()
        # write analysis to file
        with open(os.path.join(folder, f"analysis_{experiment_name}.json"), "w+") as a:
            json.dump(data, a)

def create_angel_data(network, active_angels):
    angel_data = {}
    angels = network.nodes[-network._num_angels:]
    angel_aid = network.angel_aid
    communities = network.get_communities()
    angel_aid = network.angel_aid

    angel_data["percent_active_angels"] = len(active_angels)/float(network._num_angels)
    demand_covered_by_angels = sum(len(communities[a]) * angel_aid[a] for a in active_angels)
    total_demand_of_network = sum(network.demand)
    angel_data["percent_demand_handled_by_active_angels"] = \
                demand_covered_by_angels / float(total_demand_of_network)

    entries = angel_data['angels'] = {}
    for a in angels:
        angel_entry = {}
        size_of_community = len(communities[a])
        demand_of_community = sum(network.demand[v] for v in communities[a])
        total_aid_to_community = size_of_community * angel_aid[a]

        angel_entry["isActive"] = a in active_angels
        angel_entry["num_vertices_in_community"] = size_of_community
        angel_entry["total_demand_of_community"] = demand_of_community
        angel_entry["percent_demand_handled_from_community"] = \
                        total_aid_to_community / float(demand_of_community) \
                        if demand_of_community != 0 \
                        else 0
        angel_entry["community_closeness_to_depot"] = sum(
                                    size_of_community / (network.edge_weights[0][v])
                                    for v in communities[a])
        angel_entry["average_demand_of_community"] = demand_of_community / size_of_community \
                                                    if size_of_community != 0 \
                                                    else 0
        if len(angels) > 1:
            angel_entry["community_vertex_uniqueness"] = size_of_community \
                            - max(
                                [len(set(communities[a]).intersection(communities[b])) 
                                for b in angels if a != b])

        entries[a] = angel_entry

    return angel_data

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

def create_graph_data(sol: dict, network: Network):
    data = {}
    G = nx.DiGraph()
    coords = network.get_coordinates()
    edge_weights = network.edge_weights
    edges = []
    num_nodes = len(network.nodes_with_depot)
    for i in range(num_nodes):
        for j in range(num_nodes):
            if edge_weights[i][j] < INFINITY:
                edges.append((i,j,{"weight": edge_weights[i][j]}))

    G.add_nodes_from(coords)
    G.add_edges_from(edges)
    data['closeness_centrality'] = nx.closeness_centrality(G, distance="weight")

    return data
    

def visualize_experiments(folder: str, experiment_names: str):
    if not os.path.exists(folder):
        raise Exception(f"Invalid folder path: {folder}")
    
    for x in experiment_names:
        network_path = os.path.join(folder, f"network_{x}.pickle")
        sol_path = os.path.join(folder, f"sol_{x}.json")
        network = pickle.load(open(network_path, "rb"))
        sol = json.load(open(sol_path, "rb"))
        draw(network, sol)

def clear_folder(folder: str):
    files = glob.glob(f"{folder}*")
    for f in files:
        os.remove(f)
