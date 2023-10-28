# Utility functions
import backboning  # michele
import github_api

# Standard libraries
import pandas as pd
import networkx as nx
import json
import os
import math
from pathlib import Path
from datetime import date

# Progress bar
from tqdm import tqdm


class Recommend:

    def __init__(self, path, thrs, meta_path) -> None:
        self.path = path
        self.thrs = thrs
        self.meta_path = meta_path
        self.G = None

    def load_graph(self):

        # Load given network and filter our irrelevant edges
        df = backboning.thresholding(pd.read_csv(self.path), self.thrs)

        # Load it into networkX graph
        self.G = nx.convert_matrix.from_pandas_edgelist(
            df, source="src", target="trg", edge_attr="nij")

    def add_meta_data(self):

        # load metadata
        with open(self.meta_path, "r") as fp:
            metadata = json.load(fp)

        # add metadata to graph nodes
        for repo_id, vals in metadata.items():
            to_add = {repo_id: vals}
            nx.set_node_attributes(self.G, to_add, "metadata")

    def get_node_id(self, node_name):
        """
        Returns node_id based on the provided node name.
        :node_name: str
        :return: str
        """

        return [key for key, info in dict(self.G.nodes).items() if "metadata" in info and info["metadata"]["repo_name"] == node_name][0]

    def naive_recommend(self, n, R):

        """
        Algorithm
        ---
        Find N most relevant repositories based on the edge weight of the neighboring connections to the given repository R.
        The higher the weight of the connecting edge, the better.

        Attributes
        ---
        :n: int (> 0), how many repos do you want to return
        :R: str, name of a repository for which you want to find most similar repositories
        :return: list, recommended repository names
        """

        # Get top neighbors using a naive approach
        top_edges = sorted([edge for edge in self.G.edges(self.get_node_id(R), data=True)],
                           reverse=True,
                           key=lambda edge: edge[-1]["weight"])[:n]

        # Get the top repo names
        top_repo_names = [self.G.nodes[edge[1]]["metadata"]
                          ["repo_name"] for edge in top_edges]
        
        return top_repo_names
    
    def search_depth_recommend(self, n, R, search_depth='max'):
    
        """
        Algorithm
        ---
        Let the repository for which we want to return relevant recommendations be denoted as R.
        The search_depth_recommend improves the naive_recommend by also considering repositories whose
        path length to the R is > 1. (non-neighboring repositories)

        Therefore, we assume that in certain cases a non-neighboring repository might be more relevant
        as a recommendation than a neighboring repository. More specifically, we introduce new variable W.
        W represents a weight of a theoretical edge between R and M where M is a repository whose path length
        to R is > 1. (theoretical because the edge does not indeed exist)

        Attributes
        ---
        
        """
        if search_depth == 'max':
            search_depth = math.inf


if __name__ == "__main__":
    pass
