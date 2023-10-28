import numpy as np
import pandas as pd
import networkx as nx
from tqdm import tqdm
import json
import os
import math

import backboning

def naive_recommend(G, n=5, sort_by='weight'):
    """
    The NaiveRecommend algorithm makes recommendation sorely on the neighboring repositories
    in the final recommendation graph. For each node, we consider the n neighboring
    repositories with highest edge weight, as we assume those to be the most similar, and thus
    the best recommendation. 

    Runtime: |V|*avg(k)
    Memory: |V|*n
    """

    recommendations = {}
    for node in tqdm(G.nodes()):
        sorted_neighbors = [x[0] for x in sorted(G[node].items(), 
                            key=lambda x:x[1][sort_by], reverse=True)][:n]
        recommendations[node] = sorted_neighbors

    return recommendations


def search_depth_recommend(G, n=5, sort_by='weight', search_depth='max'):
    """
    The SearchDepthRecommend improves the NaiveRecommend by also considering non-neighboring 
    repositories. It is based on the idea, that a low-weight neighboring repository is not 
    as good of a recommendation as a highly connected second level neighbor (ie. it follows
    communities of repositories).
    The algorithm is based on n calls to dijkstras on the graph subsetted to a certain search depth,
    at each node dijkstras chooses the maximum edge weight to construct the max weight path of 
    length search_depth. We then consider all possible length paths and compute a disproportional
    weighted average.
    """
    if search_depth == 'max':
        search_depth = math.inf

    recommendations = {}
    for node in tqdm(G.nodes()):
        path = [] 
        # start dijkstras with search depth
        current_search_depth = 1
        #print('current node', node)
        #print('current neighbors', list(G[node].items()))
        neighbors = G[node]
        if len(neighbors) > 0:
            max_neighbor = max(neighbors.items(), key=lambda x:x[1][sort_by])
        else: 
            recommendations[node] = []
            continue
        visited = set(G[node])
        visited.add(node)
        path.append(max_neighbor)

        while current_search_depth < search_depth:
            # find neighbors of the previous max neighbor without the node 
            max_neighbors = dict(G[max_neighbor[0]])

            # filter out all already visited neighbors
            max_neighbors = {neighbor: weight for neighbor, weight in max_neighbors.items() 
                                if neighbor not in visited}
            visited.union(set(max_neighbors.keys()))
            visited.add(max_neighbor[0])

            # stop search depth if no more neighbors
            if len(max_neighbors) == 0:
                break

            # recompute max_neighbors
            max_neighbor = max(max_neighbors.items(), key=lambda x:x[1][sort_by])
            path.append(max_neighbor)
            current_search_depth += 1

        naive_recommend = [(key, val[sort_by]) for key, val in G[node].items()]
        dijkstra_scores = list(_dijkstra_scores(path, sort_by=sort_by).items())
        all_recommend = naive_recommend + dijkstra_scores

        recommendations[node] = [x[0] for x in sorted(all_recommend, key=lambda x:x[1], reverse=True)][:n]

    return recommendations

def write_recommendation(recommendations, metadata, filepath='.', name='untitled'):
    os.makedirs(filepath) if not os.path.exists(filepath) else None

    ans = {}
    for key, val in recommendations.items():
        try: key = metadata[key]['repo_name']
        except: key = key

        try: val = [metadata[v]['repo_name'] for v in val]
        except: val = val

        ans[key] = val

    with open(f'{filepath}/{name}.json', 'w') as outfile:
        json.dump(ans, outfile)

def _dijkstra_scores(path, sort_by='weight', penalty='linear'):
    scores = {}
    for i, node in enumerate(path):
        if i == 0:
            continue
        node,_  = node
        scores[node] = 0
        for j in range(1, i+2):
            scores[node] += 1/j**2 * path[j-1][-1][sort_by]
        scores[node] /= i+1
    return scores



if __name__ == '__main__':
    # generate test recommendation system
    SIGNIF_THRS = 0.9

    print('Loading backboned')
    df = backboning.thresholding(
                pd.read_csv(f"../data/backboning/noise_corrected/hyperbolic.csv"),
                SIGNIF_THRS)
    print('Finished loading\n')


    print('Starting thresholding')
    G = nx.convert_matrix.from_pandas_edgelist(df, source="src", target="trg", 
                                               edge_attr=["nij", "score"], 
                                               create_using=nx.Graph)
    print('Finished thresholding\n')

    print('Loading Metadata')
    with open('../data/transformed/metadata.json') as infile:
        metadata = json.load(infile)
    print('Finished loading metadata\n')

    """
    weighted_edge_list = [
            [1, 3, {'nij': 0.3, 'score': 1}],
            [1, 4, {'nij': 0.01, 'score': 1}],
            [2, 3, {'nij': 0.5, 'score': 1}]
            ]

    G = nx.from_edgelist(weighted_edge_list)
    """

    print('Starting building recommendation graph')
    recommendation = search_depth_recommend(G, n=5, sort_by='nij')
    print(recommendation)
    write_recommendation(recommendation, metadata, name='search_depth_hyperbolic')
    print('done')

    #print('Naive Recommend: ', naive_recommend(G, n=2))
    #print('Search Depth Recommend: ', search_depth_recommend(G, search_depth=3))
