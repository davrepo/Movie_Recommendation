# evaluation.py 
# script holding function to evaluate the quality of recommendation based on queried metadata

# last modified     : 29/11/21
# author            : jonas-mika senghaas

import json
import os
import numpy as np
from tqdm import tqdm


#from envvars import GITHUB_TOKEN
#from github_api import ReposSummary

"""
# expected format for recommendations
metadata = {'luky/na': {'languages': [['Python', 550], ['Java', 220]]}, 
            'jonas-mika/eduml': {'languages': [['Python', 2000]]},
            'ludek/dotfiles': {'languages': [['vim', 220], ['Python', 100]]}
           }

data = {'rails/rails': ['technoweenie/restful-authentication']}

"""
def build_evaluation_metadata(metadata, attributes, filepath='.', name='evaluation_metadata'):
    os.makedirs(filepath) if not os.path.exists(filepath) else None

    ans = {}
    for key, val in metadata.items():
        try:
            nkey = metadata[key]['repo_name']
            nval = {attribute: metadata[key][attribute] for attribute in attributes}
        except: None

        ans[nkey] = nval

    with open(f'{filepath}/{name}.json', 'w') as outfile:
        json.dump(ans, outfile)



def evaluate_recommendation(recommendations, metadata, attributes, test_size=0.5, total_score=False):
    """
    function to evaluate the quality of the recommendation based on metadata.
    reads in underlying datastructure of the recommendation system (a dictionary that 
    for each repo stores a list of n recommended repos, each being stored as a dictionary
    themselves with key being the recommended repo name and values being a dict of the metadata.

    Algorithmic Idea for Evaluation:
    A 'good recommendation' is defined to be a repository that is similar in some instances to 
    the source repository. Thus, the idea is to assign a score of similarity 
    for different features of the recommended repositories, namely for:
    - languages ( len of intersection / length of union of languages for each repo)
    - tags ( len of intersectio / length of union of repos for each repo)

    the score is averaged over the n recommended repository, the per repo score is a weighted
    average. the total score is averaged over all recommendations.
    """
    n_repos = len(recommendations)


    if isinstance(test_size, int):
        random_sample_repos = np.random.choice(list(recommendations.keys()), size=test_size, replace=False) 
        random_sample = {repo: recommendations[repo] for repo in random_sample_repos} 
    elif isinstance(test_size, float):
        random_sample_repos = np.random.choice(list(recommendations.keys()), size=int(test_size*n_repos), replace=False)
        random_sample = {repo: recommendations[repo] for repo in random_sample_repos} 

    random_sample = recommendations
    attribute_scores = {attribute: None for attribute in attributes}
    for attribute in attributes:
        attribute_score = _evaluate_attribute(random_sample, 
                                              metadata, 
                                              attribute, 
                                              algorithm='jaccard', normalise=True)
        attribute_scores[attribute] = attribute_score

    if total_score:
        return np.mean(list(attribute_scores.values()))
    return attribute_scores


def _evaluate_attribute(random_sample, metadata, attribute, algorithm='jaccard', normalise=True):
    attribute_score = 0

    n_repos = len(random_sample)
    #n_recommend = len(list(random_sample.values())[0])

    # api = ReposSummary(GITHUB_TOKEN)

    src_missing = 0 
    for repo in random_sample: # maybe: subset of repos
        repo_score = 0

        src = metadata[repo] 
        #print('working on: ', repo)
        src_attr = {x[0] for x in src[attribute]}

        if src_attr == None:
            src_missing += 1
            continue

        trg_missing = 0
        n_recommend = 0
        for recommended in random_sample[repo]:
            trg = metadata[recommended]
            trg_attr = {x[0] for x in trg[attribute]}

            if trg_attr  == None:
                trg_missing += 1
                continue

            #print(src_attr, trg_attr)
            score = len(src_attr & trg_attr) / len(src_attr | trg_attr)
            #print(score)
            repo_score += score
            n_recommend += 1

        # normalise all score
        if n_recommend - trg_missing > 0:
            repo_score /= (n_recommend - trg_missing) 
        else:
            repo_score = 0
        #print(repo_score, '\n')
        attribute_score += repo_score

    # normalise summed attributes score and add total score
    if n_repos - src_missing > 0:
        attribute_score /= (n_repos - src_missing)
    else:
        attribute_score = 0

    return attribute_score


if __name__ == '__main__':
    np.random.seed(0)
    with open('../data/transformed/metadata.json') as infile:
        metadata = json.load(infile)

    build_evaluation_metadata(metadata, ['languages'],filepath='../data/evaluation/')
    with open('../data/evaluation/evaluation_metadata.json', 'r') as infile:
        metadata = json.load(infile)

    algs = ['naive_hyperbolic','search_depth_hyperbolic'] #['naive_recommend', 'search_depth']

    for alg in algs:
        with open(f'./{alg}.json', 'r') as infile:
            data = json.load(infile)

        print(alg, ':', evaluate_recommendation(data, metadata, attributes=['languages'], test_size=0.5))
