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
    angels = network.nodes[-network._num_angels:]
    for v in model.getVars():
        if v.X > 0.5:
            if v.Varname.startswith("x"):
                active_edges.append(tuple(eval(v.Varname[1:])))
            if v.Varname.startswith("z"):
                active_angels.append(eval(v.Varname[1:])[0])
    inactive_angels = [a for a in angels if a not in active_angels]

    coords = network.get_coordinates()
    active_radii = [(coords[a], network._radius) for a in active_angels]

    G = nx.DiGraph()
    G.add_nodes_from(coords)
    G.add_edges_from(active_edges)
    # num_nodes = G.number_of_nodes()

    color_map = []
    radii_nodes = []
    for n in G.nodes():
        if n in active_angels:
            color_map.append('blue')
            # radii_nodes.append((coords[n], ))  how add radii??
        elif n in inactive_angels:
            color_map.append('purple')
        elif n == 0: # depot
            color_map.append('black')
        else: # vertex
            color_map.append('red')

    nx.draw(G, 
            pos=coords, 
            node_color=color_map, 
            node_size=100, 
            with_labels=True)
    plt.show()
    

        