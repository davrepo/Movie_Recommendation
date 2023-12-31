# projections.py
# script holding function to project bipartite network onto one class

import os
import sys
import time
from datetime import date
import numpy as np
import networkx as nx
from tqdm import tqdm
import scipy as sp
from networkx.algorithms import bipartite

local_path = os.path.dirname(os.path.realpath(__file__))
if local_path not in sys.path:
    sys.path.append(local_path)

class Projections:

    def __init__(self, G, nodes) -> None:

        # User input
        self.G = G
        self.nodes = nodes

        # Utility attributes
        self.info = {
            "simple_weight": {"func": self.simple_weight, "vec": False},
            "cosine": {"func": self.cosine, "vec": True},
            "pearson": {"func": self.pearson, "vec": True},
            "hyperbolic": {"func": self.hyperbolic, "vec": False},
        }

    def simple_weight(self, u, v):
        common = set(self.G[u]) & set(self.G[v])
        return sum(self.G[u][w]['weight'] for w in common)
    
    def pearson(self, v_u, v_v):
        return sp.stats.stats.pearsonr(v_u, v_v)[0] + 1

    def cosine(self, v_u, v_v):
        return 1 - sp.spatial.distance.cosine(v_u, v_v)

    def hyperbolic(self, u, v):
        common = set(self.G[u]) & set(self.G[v])
        return sum(self.G[u][w]['weight'] / (len(set(self.G[w])) - 1) for w in common)

    def node_to_vector(self, onto, adj, u):
        index = onto.index(u)
        return np.ravel(adj.getrow(index).todense().sum(axis=0))

    def get_sparse_adj_matrix(self, rows, columns):
        return bipartite.matrix.biadjacency_matrix(self.G, rows, columns)

    def test_weight_func(self, name, info, u, v, which_n):

        if name in self.info:

            # Get the relevant projection info
            P = info["func"]
            is_vec = info["vec"]
            onto = self.nodes[which_n]

            # Compute sparse adjacency matrix if projection type requires it
            if is_vec:
                other = list(set(self.nodes.keys()) - set([which_n]))[0]
                adj = self.get_sparse_adj_matrix(onto, self.nodes[other])
            else:
                adj = None

            # Compute weight
            if is_vec:
                v_u = self.node_to_vector(onto, adj, u)
                v_v = self.node_to_vector(onto, adj, v)
                w = P(v_u, v_v)
            else:
                w = P(u, v)

            # Delete Adjacency graph from memory since you no longer need it
            del adj

            return w

        else:
            raise SyntaxError(
                f"Projection {name} does not exist within our projections. Please use one of these: {', '.join(list(self.info.keys()))}.")

    def project(self, which_n, which_p, savepath):
        """
        Custom function to perform projections.

        Algorithm
        1A Use double for loop to iterate over all unique pairs of nodes and compute edge weight according to weight function.
        1B Save each computed eddge to the given edgelist

        :G: bi-partite graph
        :which_n: str, which type of nodes to project graph onto
        :which_p: str, which projection to use
        :savepath: str, where to save the created edge list
        :return: None
        """

        if which_p in self.info:

            # Get the relevant projection info
            P = self.info[which_p]["func"]
            is_vec = self.info[which_p]["vec"]
            onto = self.nodes[which_n]

            # Define constaint whether to accept computed weight or not
            w_constraint = self.info[which_p].get("constr_w")
            if not w_constraint:
                def w_constraint(w): return w > 0

            # Compute sparse adjacency matrix if projection type requires it
            if is_vec:
                other = list(set(self.nodes.keys()) - set([which_n]))[0]
                adj = self.get_sparse_adj_matrix(onto, self.nodes[other])
            else:
                adj = None

            # Overwrite the old content first with blank string
            with open(savepath, 'w') as outfile:
                outfile.write("")

            # Append the computed edges into the savepath file
            with open(savepath, 'a') as outfile:

                # Add a header
                outfile.write("src\ttrg\tweight\n")

                # Iterate over all combinations of nodes which you want to project onto
                for u in tqdm(onto):
                    nbrs2 = {n for nbr in set(self.G[u])
                             for n in self.G[nbr]} - {u}
                    for v in nbrs2:

                        # Compute weight for given edge (if any)
                        if is_vec:
                            v_u = self.node_to_vector(onto, adj, u)
                            v_v = self.node_to_vector(onto, adj, v)
                            w = P(v_u, v_v)
                        else:
                            w = P(u, v)

                        # If it passes constraint, save it
                        if w_constraint(w):
                            # Save the edge (tab-separated)
                            outfile.write(f"{u}\t{v}\t{w}\n")

            # Delete Adjacency graph from memory since you no longer need it
            del adj

        else:
            raise SyntaxError(
                f"Projection {which_p} does not exist within our projections. Please use one of these: {', '.join(list(self.info.keys()))}.")


if __name__ == '__main__':

    # Define G
    G = nx.read_edgelist(f"../data/transformed/data.txt",
                         delimiter=",", create_using=nx.Graph)

    # Define user and item nodes
    user = [node for node in G.nodes() if node[0] == 'user']
    item = [node for node in G.nodes() if node[0] == 'item']

    # Initiate projections object
    proj = Projections(G, nodes={"user": user, "item": item})

    # Define u and v
    u = "r1"
    v = "r2"

    # Test
    proj.project(which_n="user", which_p="simple_weight",
                 savepath=f"../data/projections/edge_list_format/simple_weight.edges")
    
    