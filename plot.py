import matplotlib.pyplot as plt
import networkx as nx
from gurobipy import Model
from network import Network

def draw(network: Network, model: Model) -> None:
    """
    Draws the solution. Assumes model is a solved model.
    """
    active_edges = []
    active_angels = []
    for v in model.getVars():
        if v.X > 0.5:
            if v.Varname.startswith("x"):
                active_edges.append(tuple(eval(v.Varname[1:])))
            if v.Varname.startswith("z"):
                active_angels.append(eval(v.Varname[1:])[0])
    
    G = nx.DiGraph()
    coords = network.get_coordinates()
    G.add_nodes_from(coords)
    G.add_edges_from(active_edges)

    color_map = []
    for n in G.nodes():
        if n in active_angels:
            color_map.append('blue')
        elif n == 0:
            color_map.append('black')
        else:
            color_map.append('red')

    nx.draw(G, 
            pos=coords, 
            node_color=color_map, 
            node_size=100, 
            with_labels=True)
    plt.show()
    

        