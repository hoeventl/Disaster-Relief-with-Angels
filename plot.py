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
    radii_coords = [coords[a] for a in angels]

    G = nx.DiGraph()
    G.add_nodes_from(coords)
    G.add_edges_from(active_edges)

    color_map = []
    for n in G.nodes():
        if n in active_angels:
            color_map.append('blue')
        elif n in inactive_angels:
            color_map.append('purple')
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
        color = 'blue' if a in active_angels else 'purple'
        c = plt.Circle(radii_coords[count], 
                       radius=network._radius[count], 
                       fill=False, 
                       color=color,
                       linestyle='--')
        ax.add_patch(c)
        count = count+1
    plt.axis('equal')

    plt.show()
    

        