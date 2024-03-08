import matplotlib.pyplot as plt
import networkx as nx
import pickle, json
from gurobipy import Model
from network import Network

def draw(network: Network, model: Model) -> None:
    """
    Draws the solution.
    """
    active_edges = []
    active_angels = []
    
    for v in model.getVars():
        if v.X > 0.5:
            if v.Varname.startswith("x"):
                active_edges.append(tuple(eval(v.Varname[1:])))
            if v.Varname.startswith("z"):
                active_angels.append(eval(v.Varname[1:])[0])
    
    _draw(network, active_edges, active_angels)
    
def draw(network_path: str, sol_path: str) -> None:
    network = pickle.load(open(network_path, "rb"))
    sol = json.load(open(sol_path, "rb"))

    active_edges = []
    active_angels = []
    for v in sol["Vars"]:
        if v['X'] > 0.5:
            if v['VarName'].startswith("x"):
                active_edges.append(tuple(eval(v['VarName'][1:])))
            if v['VarName'].startswith("z"):
                active_angels.append(eval(v['VarName'][1:])[0])
                
    _draw(network, active_edges, active_angels)

def _draw(network: Network, active_edges: list[tuple], active_angels: list) -> None:
    angels = network.nodes[-network._num_angels:]
    inactive_angels = [a for a in angels if a not in active_angels]

    coords = network.get_coordinates()
    radii_coords = [coords[a] for a in angels]

    G = nx.DiGraph()
    G.add_nodes_from(coords)
    G.add_edges_from(active_edges)

    color_map = []
    for n in G.nodes():
        if n in active_angels:
            color_map.append('blue')
        elif n in inactive_angels:
            color_map.append('lightblue')
        elif n == 0: # depot
            color_map.append('black')
        else: # vertex
            color_map.append('red')
    nx.draw(G, 
            pos=coords,
            labels={i:i+1 for i in range(G.number_of_nodes())},
            node_color=color_map, 
            node_size=100)
    
    # add radii around angels
    ax = plt.gca()
    count = 0
    for a in angels:
        color = 'blue' if a in active_angels else 'lightblue'
        c = plt.Circle(radii_coords[count], 
                       radius=network._radius[count], 
                       fill=False, 
                       color=color,
                       linestyle='--')
        ax.add_patch(c)
        count = count+1
    plt.axis('equal')

    plt.show()

        