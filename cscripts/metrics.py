# metrics.py 
# script holding function to analyse unipartite and bipartite networkx

# last modified     : 16/11/21
# author            : jonas-mika senghaas

import os
import sys
import time
from datetime import date
from collections import Counter
import numpy as np
import pandas as pd
import networkx as nx
from tqdm import tqdm

local_path = os.path.dirname(os.path.realpath(__file__))
if local_path not in sys.path:
    sys.path.append(local_path)

from handle_timeout import * 

#--- GLOBAL SETUP 
STOP_EXECUTION = 60 
np.set_printoptions(suppress=True)



#--- HELPER FUNCTIONS
def five_num_summary(arr):
    """
    Function to compute a five-number-summary of any given 1-dimensional data, 
    that is passed in as an iterable. Uses numpy's percentile() function.

    Function Arguments 
    ------------------
    arr : iterable  |   1D Data

    Returns
    -------
    np.array(5)     |   Five-Number Summary of Data

    """

    return np.percentile(arr, [0, 25, 50, 75, 100])

@break_after(STOP_EXECUTION)
def get_degrees(G):
    """
    Function to extract an (unsorted) iterable of all degrees from a
    nx.Graph object. Uses nx.Graph degree() method.

    Function Arguments 
    ------------------
    G : nx.Graph                |   Graph 

    Returns
    -------
    degrees : iterable          |   Unsorted Degrees of Graph 
    """

    return [degree for _, degree in G.degree()]

@break_after(10)
def get_lccs(G):
    """
    Function to extract an (unsorted) iterable of all local clustering
    coefficients from a nx.Graph object. Uses nx.clustering function.
    Note: Computationally expensive, may abort on huge graphs.

    Function Arguments 
    ------------------
    G : nx.Graph                |   Graph 

    Returns
    -------
    lccs : iterable             |   Unsorted LCC's of Graph 
    """

    return list(nx.clustering(G).values())

@break_after(STOP_EXECUTION)
def get_ccs(G):
    """
    Function to extract an  iterable of all connected components
    (disconnected) nx.Graph object. Uses nx.connected_components() function.

    Function Arguments 
    ------------------
    G : nx.Graph                |   Graph 

    Returns
    -------
    ccs : iterable(nx.Graph)    |   Unsorted LCC's of Graph 
    """

    return [G.subgraph(cc) for cc in nx.connected_components(G)]


@break_after(STOP_EXECUTION)
def get_edge_weights(G):
    """
    Function to extract an iterable of all edge_weights from a 
    nx.Graph object. 

    Function Arguments 
    ------------------
    G : nx.Graph                |   Graph 

    Returns
    -------
    edge_weights : iterable(float) |   Iterable of edge weights 
    """
    if not nx.is_weighted(G):
        return None
    return [edge[-1]['weight'] for edge in G.edges(data=True)] 



#--- SINGLE NETWORK METRICS

# basic network statistics
@break_after(STOP_EXECUTION)
def number_of_nodes(G):
    """
    Returns number of nodes in graph. Uses number_of_nodes() 
    method on  nx.Graph object.

    Function Arguments 
    ------------------
    G : nx.Graph                |   Graph 

    Returns
    -------
    node_count : int            |   Number of Nodes
    """

    return G.number_of_nodes()

@break_after(STOP_EXECUTION)
def number_of_edges(G):
    """
    Returns number of edges in graph. Uses number_of_edges() 
    method on  nx.Graph object.

    Function Arguments 
    ------------------
    G : nx.Graph                |   Graph 

    Returns
    -------
    edge_count : int            |   Number of Edges
    """

    return G.number_of_edges()

@break_after(STOP_EXECUTION)
def global_density(G):
    """
    Returns global density of graph, which is the proportion of
    the number of existing edges of from all edges that can
    possibly exist, st. for an undirected graph:

    density = |E| / N(N-1)

    Function Arguments 
    ------------------
    G : nx.Graph                |   Graph 

    Returns
    -------
    density : float[0,1]        |   Global Density Measure 
    """
    return nx.density(G)

@break_after(STOP_EXECUTION)
def global_diameter(G):
    """
    Returns global diameter, which corresponds to the 
    longest shortest path in the network. Can only be computed
    for fully connected graphs. Otherwise, callable on CCs (ie.
    largest CC)

    Function Arguments 
    ------------------
    G : nx.Graph                |   Graph 

    Returns
    -------
    diameter : int              |   Global Diameter Measure 
    """
    if nx.is_connected(G):
        return nx.diameter(G)
    else: return 'No Global Diameter (Unconnected Graph)'

# edge weights statistics
@break_after(STOP_EXECUTION)
def average_edge_weight(edge_weights):
    return np.mean(edge_weights) if edge_weights else None

@break_after(STOP_EXECUTION)
def summarise_edge_weights(edge_weights):
    return five_num_summary(edge_weights) if edge_weights else None

@break_after(STOP_EXECUTION)
def variance_edge_weights(edge_weights):
    return np.var(edge_weights) if edge_weights else None

@break_after(STOP_EXECUTION)
def most_frequent_edge_weight(edge_weights):
    return Counter(edge_weights).most_common()[0][0] if edge_weights else None

# degree statistics
@break_after(STOP_EXECUTION)
def average_degree(degrees):
    """
    Returns average degree from iterable of degrees.

    Function Arguments 
    ------------------
    degrees : iterable(int)     |   Iterable of Degrees 

    Returns
    -------
    average_degree : float      |   Average Degree 
    """

    return np.mean(degrees) if degrees else None

@break_after(STOP_EXECUTION)
def summarise_degrees(degrees):
    """
    Returns Five-Number-Summary of Degrees from iterable
    of degrees.

    Function Arguments 
    ------------------
    degrees : iterable(int)     |   Iterable of Degrees 

    Returns
    -------
    summary : np.array(5)       |   Five-Num-Summary of Degrees 
    """

    return five_num_summary(degrees) if degrees else None



# local clustering coefficient
@break_after(STOP_EXECUTION)
def average_lcc(lccs):
    """
    Returns average local clustering coefficient from 
    iterable of local clustering coefficients.

    Function Arguments 
    ------------------
    lccs : iterable(float)      |   Iterable of LCCs 

    Returns
    -------
    average_lcc : float         |   Average LCC 
    """

    return np.mean(lccs) if lccs else None

@break_after(STOP_EXECUTION)
def summarise_lcc(lccs):
    """
    Returns Five-Number-Summary of local clustering 
    coefficients from iterable of local clustering 
    coefficients.

    Function Arguments 
    ------------------
    lccs : iterable(float)      |   Iterable of LCCs 

    Returns
    -------
    summary : np.array(5)       |   Five-Num-Summary of LCCs
    """

    return five_num_summary(lccs) if lccs else None



# connected components (size)
@break_after(STOP_EXECUTION)
def number_of_ccs(ccs):
    """
    Returns number of connected components from iterable
    of connected subgraphs. 

    Function Arguments 
    ------------------
    ccs : iterable(nx.Graph)    |   Iterable of connected subgraphs 

    Returns
    -------
    #ccs : int                  |  Number of CCs 
    """

    return len(ccs) if ccs else None

@break_after(STOP_EXECUTION)
def average_cc_size(ccs):
    """
    Returns Average Size of connected components from iterable
    of connected components as nx.Subgraphs().

    Function Arguments 
    ------------------
    ccs : iterable(nx.Graph)    |   Iterable of connected subgraphs 

    Returns
    -------
    average_size : float        |  Average Size of CCs
    """

    return np.mean([cc.number_of_nodes() for cc in ccs]) if ccs else None

@break_after(STOP_EXECUTION)
def summarise_cc_size(ccs):
    """
    Returns Five-Number-Summary of sizes of connected components 
    from iterableof connected components as nx.Subgraphs().

    Function Arguments 
    ------------------
    ccs : iterable(nx.Graph)    |   Iterable of connected subgraphs 

    Returns
    -------
    summary : np.array(5)       |   Five-Num-Summary of CC Sizes
    """

    return five_num_summary([cc.number_of_nodes() for cc in ccs]) if ccs else None

@break_after(STOP_EXECUTION)
def average_cc_density(ccs):
    """
    Returns the average density in all connected components.

    Function Arguments 
    ------------------
    ccs : iterable(nx.Graph)    |   Iterable of connected subgraphs 

    Returns
    -------
    average_density : float     |   Average Density among all CCs
    """

    return np.mean([nx.density(cc) for cc in ccs]) if ccs else None

@break_after(STOP_EXECUTION)
def summarise_cc_density(ccs):
    """
    Returns Five-Number-Summary of densities in all connected components.

    Function Arguments 
    ------------------
    ccs : iterable(nx.Graph)    |   Iterable of connected subgraphs 

    Returns
    -------
    summary : np.array(5)       |   Five-Num-Summary of Densities among all CCs
    """
    return five_num_summary([nx.density(cc) for cc in ccs]) if ccs else None

@break_after(STOP_EXECUTION)
def average_diameter(ccs):
    """
    Returns average diameter of all connected components.

    Function Arguments 
    ------------------
    ccs : iterable(nx.Graph)     |   Iterable of connected subgraphs 

    Returns
    -------
    average_diameter : float     |   Average Diameter among all CCs
    """

    return np.mean([nx.diameter(cc) for cc in ccs]) if ccs else None

@break_after(STOP_EXECUTION)
def summarise_diameter(ccs):
    """
    Returns Five-Number-Summary of diameter in all connected components.

    Function Arguments 
    ------------------
    ccs : iterable(nx.Graph)    |   Iterable of connected subgraphs 

    Returns
    -------
    summary : np.array(5)       |   Five-Num-Summary of diameters among all CCs
    """
    return five_num_summary([nx.diameter(cc) for cc in ccs]) if ccs else None



# centrality measures
@break_after(STOP_EXECUTION)
def degree_centrality(G, n):
    """
    Returns the n most degree central nodes from a nx.Graph.

    Function Arguments 
    ------------------
    G : nx.Graph                |   Graph 
    n : int                     |   Number of nodes to return

    Returns
    -------
    nodes : iterable(node)      |   N most degree central nodes  
    """
    return [x[0] for x in sorted([item for item in nx.algorithms.centrality.degree_centrality(G).items()], 
                key=lambda item: item[1], reverse=True)[:n]]

@break_after(10)
def betweenness_centrality(G, n):
    """
    Returns the n nodes with highest betweenness centrality 
    from a nx.Graph.

    Function Arguments 
    ------------------
    G : nx.Graph                |   Graph 
    n : int                     |   Number of nodes to return

    Returns
    -------
    nodes : iterable(node)      |   N most between nodes
    """
    return [x[0] for x in sorted([item for item in nx.algorithms.centrality.betweenness_centrality(G).items()], 
                key=lambda item: item[1], reverse=True)[:n]]




#--- NETWORK STATISTIC BUNDLER
#--- Combines functions in similar fields into dictionary to conveniently call together (also faster in execution)
def export_metrics(G):
    degrees = get_degrees(G)
    lccs = get_lccs(G)
    try: 
        ccs = get_ccs(G)
    except: 
        ccs = None
    edge_weights = get_edge_weights(G)
    try: gd = global_diameter(G)
    except: gd = None

    return {'Basic Statistics': 
                 {
                 'Number of Nodes': number_of_nodes(G), 
                 'Number of Edges': number_of_edges(G), 
                 'Global Density' : global_density(G),
                 'Global Diameter': gd
                    #'Average Diameter': f'{round(average_diameter(G), 2)}', 'Five-Number-Summary Diameter': summarise_diameter(G)}
                 },
            'Degree Statistics': 
                {
                'Average Degree': average_degree(degrees),
                'Five-Number-Summary Degrees': summarise_degrees(degrees)
                },
            'Edge Weight Statistics':
                {
                'Average Edge Weight': average_edge_weight(edge_weights),
                'Five-Number-Summary Edge Weights': summarise_edge_weights(edge_weights),
                'Variance of Edge Weights': variance_edge_weights(edge_weights),
                'Most Frequent Edge Weight': most_frequent_edge_weight(edge_weights)
                },
            'Clustering Statistics':
                {
                'Average LCC': average_lcc(lccs),
                'Five-Number-Summary LCC': summarise_lcc(lccs)
                },
            'Connected Components Statistics': 
                {
                 'Number of CC': number_of_ccs(ccs), 
                 'Average CC Size': average_cc_size(ccs), 
                 'Five-Number-Summary of CC Sizes': summarise_cc_size(ccs),
                 'Average CC Density': average_cc_density(ccs),
                 'Five-Number-Summary of CC Densities': summarise_cc_density(ccs)
                },
            'Centrality Statistics':
                {
                'Degree Centrality': degree_centrality(G, 10),
                'Betweenness Centrality': betweenness_centrality(G, 10)
                }
            }


if __name__ == '__main__':
    start = time.time()
    G = nx.read_gpickle('../data/projections/pickle_format/simple_weight.pickle')
    #G = nx.karate_club_graph()
    end = time.time()
    print(f'Finished Reading in {end-start}s')

    print(export_metrics(G))
