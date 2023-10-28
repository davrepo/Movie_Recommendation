import networkx as nx
import json
from tqdm import tqdm

G = nx.read_edgelist("../data/transformed/data.txt", delimiter=",", comments='#', create_using=nx.Graph) 


with open('../webapp/public/data/naive_hyperbolic.json') as infile:
    recommendations = json.load(infile)
with open('../data/transformed/metadata.json') as infile:
    metadata = json.load(infile)


def avgDegreeRecommendations(recommendations):
    sum_ = 0
    n = 0
    for key,values in tqdm(recommendations.items()):
        n += 1

        degrees = 0
        for recommended in values:

            degrees += G.degree[recommended]

        sum_ += degrees / len(values) 
    
    return sum_ / n


#print(avgDegreeRecommendations(recommendations))


