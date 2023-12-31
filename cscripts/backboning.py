##########################################################################
# This entire module was downloaded from: https://www.michelecoscia.com/?page_id=287
##########################################################################

import sys
import warnings
import numpy as np
import pandas as pd
import networkx as nx
from collections import defaultdict
from scipy.stats import binom


def read(filename, column_of_interest, triangular_input=False, consider_self_loops=True, undirected=False, drop_zeroes=True, sep="\t"):
    """Reads a field separated input file into the internal backboning format (a Pandas Dataframe).
    The input file should have three or more columns (default separator: tab).
    The input file must have a one line header with the column names.
    There must be two columns called 'src' and 'trg', indicating the origin and destination of the interaction.
    All other columns must contain integer or floats, indicating the edge weight.
    In case of undirected network, the edges have to be present in both directions with the same weights, or set triangular_input to True.

    Args:
    filename (str): The path to the file containing the edges.
    column_of_interest (str): The column name identifying the weight that will be used for the backboning.

    KWArgs:
    triangular_input (bool): Is the network undirected and are the edges present only in one direction? default: False
    consider_self_loops (bool): Do you want to consider self loops when calculating the backbone? default: True
    undirected (bool): Is the network undirected? default: False
    drop_zeroes (bool): Do you want to keep zero weighted connections in the network? Important: it affects methods based on degree, like disparity_filter. default: False
    sep (char): The field separator of the inout file. default: tab

    Returns:
    The parsed network data, the number of nodes in the network and the number of edges.
    """
    table = pd.read_csv(filename, sep=sep)
    table = table[["src", "trg", column_of_interest]]
    table.rename(columns={column_of_interest: "nij"}, inplace=True)
    if drop_zeroes:
        table = table[table["nij"] > 0]
    if not consider_self_loops:
        table = table[table["src"] != table["trg"]]
    if triangular_input:
        table2 = table.copy()
        table2["new_src"] = table["trg"]
        table2["new_trg"] = table["src"]
        table2.drop("src", 1, inplace=True)
        table2.drop("trg", 1, inplace=True)
        table2 = table2.rename(columns={"new_src": "src", "new_trg": "trg"})
        table = pd.concat([table, table2], axis=0)
        table = table.drop_duplicates(subset=["src", "trg"])
    original_nodes = len(set(table["src"]) | set(table["trg"]))
    original_edges = table.shape[0]
    if undirected:
        return table, original_nodes, original_edges / 2
    else:
        return table, original_nodes, original_edges


def thresholding(table, threshold):
    """Reads a preprocessed edge table and returns only the edges supassing a significance threshold.

    Args:
    table (pandas.DataFrame): The edge table.
    threshold (float): The minimum significance to include the edge in the backbone.

    Returns:
    The network backbone.
    """
    table = table.copy()
    if "sdev_cij" in table:
        return table[(table["score"] - (threshold * table["sdev_cij"])) > 0][["src", "trg", "nij", "score"]]
    else:
        return table[table["score"] > threshold][["src", "trg", "nij", "score"]]


def write(table, network, method, folder):
    if not table.empty and "src" in table:
        table.to_csv("%s/%s_%s.csv" %
                     (folder, network, method), sep="\t", index=False)
    else:
        warnings.warn(
            "Incorrect/empty output. Nothing written on disk", RuntimeWarning)


# def stability_jac(table1, table2):
#     table1_edges = set(zip(table1["src"], table1["trg"]))
#     table2_edges = set(zip(table2["src"], table2["trg"]))
#     return float(len(table1_edges & table2_edges)) / len(table1_edges | table2_edges)


# def stability_corr(table1, table2, method="spearman", log=False, what="nij"):
#     corr_table = table1.merge(table2, on=["src", "trg"])
#     corr_table = corr_table[["%s_x" % what, "%s_y" % what]]
#     if log:
#         corr_table["%s_x" % what] = np.log(corr_table["%s_x" % what])
#         corr_table["%s_y" % what] = np.log(corr_table["%s_y" % what])
#     return corr_table["%s_x" % what].corr(corr_table["%s_y" % what], method=method)


# def test_densities(table, start, end, step):
#     if start > end:
#         raise ValueError("start must be lower than end")
#     steps = []
#     x = start
#     while x <= end:
#         steps.append(x)
#         x += step
#     onodes = len(set(table["src"]) | set(table["trg"]))
#     oedges = table.shape[0]
#     oavgdeg = (2.0 * oedges) / onodes
#     for s in steps:
#         edge_table = thresholding(table, s)
#         nodes = len(set(edge_table["src"]) | set(edge_table["trg"]))
#         edges = edge_table.shape[0]
#         avgdeg = (2.0 * edges) / nodes
#         yield (s, nodes, (100.0 * nodes) / onodes, edges, (100.0 * edges) / oedges, avgdeg, avgdeg / oavgdeg)


def disparity_filter(table, undirected=False, return_self_loops=False):
    sys.stderr.write("Calculating DF score...\n")
    table = table.copy()
    table_sum = table.groupby(table["src"]).sum().reset_index()
    table_deg = table.groupby(table["src"]).count()["trg"].reset_index()
    table = table.merge(table_sum, on="src", how="left", suffixes=("", "_sum"))
    table = table.merge(table_deg, on="src", how="left",
                        suffixes=("", "_count"))
    table["score"] = 1.0 - \
        ((1.0 - (table["nij"] / table["nij_sum"])) ** (table["trg_count"] - 1))
    table["variance"] = (table["trg_count"] ** 2) * (((20 + (4.0 * table["trg_count"])) / ((table["trg_count"] + 1.0)
                                                                                           * (table["trg_count"] + 2) * (table["trg_count"] + 3))) - ((4.0) / ((table["trg_count"] + 1.0) ** 2)))
    if not return_self_loops:
        table = table[table["src"] != table["trg"]]
    if undirected:
        table["edge"] = table.apply(
            lambda x: "%s-%s" % (min(x["src"], x["trg"]), max(x["src"], x["trg"])), axis=1)
        table_maxscore = table.groupby(by="edge")["score"].max().reset_index()
        table_minvar = table.groupby(by="edge")["variance"].min().reset_index()
        table = table.merge(table_maxscore, on="edge", suffixes=("_min", ""))
        table = table.merge(table_minvar, on="edge", suffixes=("_max", ""))
        table = table.drop_duplicates(subset=["edge"])
        table = table.drop("edge", 1)
        table = table.drop("score_min", 1)
        table = table.drop("variance_max", 1)
    return table[["src", "trg", "nij", "score", "variance"]]