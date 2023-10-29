# a set of pre-defined experiment creation functions
from network import Network

def one_for_all() -> Network:
    # currently will make one angel in a random shadow location but covers all nodes
    # would like to decide amount of aid too
    n = Network("Instances/A-n32-k5.vrp", num_angels=0, radius="max")
    

    # scrap this, just use an instance from vrp set A or set B... see downloads
    # then add an angel
    # much easier to use existing code

    return n