import matplotlib.pyplot as plt
import networkx as nx
import scipy
import pandas as pd
import numpy as np
import igraph as ig
from statistics import mean

# 2 TODO s in script, search for "TODO"
# run on cluster with laurasbash-nw.sh

netnumber = 5000 # TODO: how many networks to generate?

np.set_printoptions(suppress=True)
pd.set_option('display.float_format', str)

def _random_subset(seq, m, rng):
    """Return m unique elements from seq.

    This differs from random.sample which can return repeated
    elements if seq holds repeated elements.

    Note: rng is a random.Random or numpy.random.RandomState instance.
    """
    targets = set()
    
    while len(targets) < m:
        x = rng.choice(seq)
        targets.add(x)
    return targets

    # from networkx source code, amended
def barabasi_albert_graph(n, m, seed=None, initial_graph=None):
    """Returns a random graph using Barabási–Albert preferential attachment

    A graph of $n$ nodes is grown by attaching new nodes each with $m$
    edges that are preferentially attached to existing nodes with high degree.

    Parameters
    ----------
    n : int
        Number of nodes
    m : int
        Number of edges to attach from a new node to existing nodes
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    initial_graph : Graph or None (default)
        Initial network for Barabási–Albert algorithm.
        It should be a connected graph for most use cases.
        A copy of `initial_graph` is used.
        If None, starts from a star graph on (m+1) nodes.

    Returns
    -------
    G : Graph

    Raises
    ------
    NetworkXError
        If `m` does not satisfy ``1 <= m < n``, or
        the initial graph number of nodes m0 does not satisfy ``m <= m0 <= n``.

    References
    ----------
    .. [1] A. L. Barabási and R. Albert "Emergence of scaling in
       random networks", Science 286, pp 509-512, 1999.
    """

    if m < 1 or m >= n:
        raise nx.NetworkXError(
            f"Barabási–Albert network must have m >= 1 and m < n, m = {m}, n = {n}"
        )

    if initial_graph is None:
        # Default initial graph : star graph on (m + 1) nodes
        G = nx.star_graph(m)
    else:
        if len(initial_graph) < m or len(initial_graph) > n:
            raise nx.NetworkXError(
                f"Barabási–Albert initial graph needs between m={m} and n={n} nodes"
            )
        G = initial_graph.copy()

    # List of existing nodes, with nodes repeated once for each adjacent edge
    repeated_nodes = [n for n, d in G.in_degree() for _ in range(d)]
    # Start adding the other n - m0 nodes.
    source = len(G)
    while source < n:
        # print(source)
        # print("source")
        # Now choose m unique nodes from the existing nodes
        # Pick uniformly from repeated_nodes (preferential attachment)
        targets = _random_subset(repeated_nodes + list(G.nodes), m, seed) # add +list(G.nodes) so that also 0-in.degree nodes "could" get sampled
        #print(repeated_nodes + list(G.nodes))
        #print("targets")
        # Add edges to m nodes from the source.
        G.add_edges_from(zip([source] * m, targets))
        #print("add edges")
        # Add one node to the list for each new edge just created.
        repeated_nodes.extend(targets)
    
        #print(repeated_nodes)
        #print("add target nodes to repeated lists")
        # And the new node "source" has m edges to add to the list.
        
        # repeated_nodes.extend([source] * m) # Laura: comment out so outgoing degree is not reflected in preferential sampling from repeated nodes 

        source += 1
    return G


def gennw(i):
    np.random.seed(i)
    rng = np.random.default_rng() 
    import random
    random.seed(i)        # or any integer
    
    m = 3
    size = 1000 # number of nodes   

    # Initial network to be fed into amended BA-function
    D = nx.complete_graph(m, nx.DiGraph())
    # D.degree
    G = barabasi_albert_graph (size, m, rng, D)
    #nx.draw(G, with_labels=True)   
    # Check avergae clustering coefficient and average out-degree
    G_edgelist = nx.generate_edgelist(G) # to create new undirected graph to compute clustering coeff 
    G_undir = nx.parse_edgelist(G_edgelist)

    goalcoeff = .29 # retrieved from empirical data, see below
    clustercoeff = nx.average_clustering(G_undir)

    while clustercoeff < goalcoeff:
        # 0 sample source node
        source = random.sample(G.nodes,1)[0]    
        
        # 1 sample 1 friend of source node
        if G.out_degree(source) > 1:  # only edges originating from these nodes: outgoing edges: befriending
            friend_of_source = random.sample([n for n in G.neighbors(source)],1)[0]
        else: 
            friend_of_source = [n for n in G.neighbors(source)][0]
        
        # 2 sample a friend of the friend, not source
        if G.out_degree(friend_of_source) > 1:
            friend_of_friend = random.sample([n for n in G.neighbors(friend_of_source)],1)[0]
        else: 
            friend_of_friend = [n for n in G.neighbors(friend_of_source)][0]
        
        # 3 add edge from the friend's friend to source node (if not source node chosen)
        if source != friend_of_friend:
            G.add_edge(source,friend_of_friend, color='r')
        
            G_edgelist = nx.generate_edgelist(G)
            G_undir = nx.parse_edgelist(G_edgelist)
            clustercoeff = nx.average_clustering(G_undir)
    
    network_name = f'networks/NW_{i}.gml'
    nx.write_gml(G, network_name)


import multiprocessing as mp

                                                        
if __name__ == '__main__':
    N = 40 #TODO: select how many cores to parallelize on

    inputs = list(range(0,netnumber,1))

    with mp.Pool(processes = N) as p:
        results = p.map(gennw, inputs)