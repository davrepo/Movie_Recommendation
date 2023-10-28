# plotting.py
# script holding function to analyse unipartite and bipartite networkx

# last modified     : 16/11/21
# author            : jonas-mika senghaas

import metrics
import powerlaw as pl
from tqdm import tqdm
import networkx as nx
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
import sys
from time import time
from collections import Counter

# allow imports locally (without referring to module structure)
local_path = os.path.dirname(os.path.realpath(__file__))
if local_path not in sys.path:
    sys.path.append(local_path)


# global settings
sns.set_style("darkgrid");
sns.set(rc={"xtick.bottom": True, "ytick.left": True});


def plot_single_degree_distribution(degrees, name='', ax=None, figsize=(5, 5), scale='linear'):
    if ax == None:
        _, ax = plt.subplots(figsize)

    counter = Counter(degrees)
    data = pd.DataFrame(list(counter.items()), columns=(
        "k", "count")).sort_values(by="k")

    sns.scatterplot(data=data, x='k', y='count',
                    ax=ax,
                    alpha=0.6);

    ax.set_title(
        f"Degree Distribution of\n{name.title()} ({scale.title()}-Scale)", weight="bold")
    ax.set(xlabel='Degrees ($k$)', ylabel='Counts')

    if scale == 'log':
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlim(10**0*0.9, 10**5)
    elif scale != 'linear':
        return None

    return ax


def plot_degree_distribution(*degrees, names=None, scales='linear', figsize=(5, 5)):
    if names == None:
        names = ['Unnamed' for _ in range(len(degrees))]
    if type(scales) == str:
        scales = [scales]

    # initialising subplots figure
    n_rows = len(degrees)
    n_cols = len(scales)

    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(figsize[0]*n_cols, figsize[1]*n_rows),
                            constrained_layout=True)

    # formatting axes array
    axs = np.array(axs)
    if n_rows > 1 and n_cols == 1:
        axs = axs.reshape(-1, 1)
    elif n_rows == 1 and n_cols > 1:
        axs = axs.reshape(1, -1)
    elif n_rows == 1 and n_cols == 1:
        axs = axs.reshape(1, 1)

    for i, degree, name in zip(range(n_rows), degrees, names):
        for j, s in zip(range(n_cols), scales):
            fig = plot_single_degree_distribution(degree, name,
                                                  figsize=figsize,
                                                  ax=axs[i][j],
                                                  scale=s)

    return fig


def plot_single_ccdf_degrees(degrees, fit=True, name='', ax=None, figsize=(5, 5), scale='log'):
    if ax == None:
        _, ax = plt.subplots(figsize)

    counter = Counter(degrees)
    data = pd.DataFrame(list(counter.items()), columns=(
        "k", "count")).sort_values(by="k", ascending=False)

    # computing ccdf
    data["cumsum"] = data["count"].cumsum()
    data["ccdf"] = data["cumsum"] / data["count"].sum()
    data = data[["k", "ccdf"]].sort_values(by="k")

    # computing powerlaw fit
    if fit:
        results = pl.Fit(data["ccdf"], verbose=False, discrete=True)
        data["fit"] = (10**results.power_law.Kappa) * \
            (data["k"] ** -results.power_law.alpha)

    sns.lineplot(data=data, x='k', y='ccdf', ax=ax);
    if fit:
        sns.lineplot(data=data, x='k', y='fit', ax=ax);

    ax.set_title(
        f"CCDF Degree Distribution of\n{name.title()} ({scale.title()}-Scale)", weight="bold")
    ax.set(xlabel='Degrees ($k$)', ylabel='CCDF (P(X>=k))')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(10**0, data['k'].max())

    return ax


def plot_ccdfs_degrees(*degrees, names=None, fit=True, figsize=(5, 5)):
    if names == None:
        names = ['Unnamed' for _ in range(len(degrees))]
    if type(fit) == bool:
        fit = [fit]

    # initialising subplots figure
    n_rows = len(degrees)
    n_cols = len(fit)

    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(figsize[0]*n_cols, figsize[1]*n_rows),
                            constrained_layout=True)

    # formatting axes array
    axs = np.array(axs)
    if n_rows > 1 and n_cols == 1:
        axs = axs.reshape(-1, 1)
    elif n_rows == 1 and n_cols > 1:
        axs = axs.reshape(1, -1)
    elif n_rows == 1 and n_cols == 1:
        axs = axs.reshape(1, 1)

    for i, degree, name in zip(range(n_rows), degrees, names):
        for j, f in zip(range(n_cols), fit):
            fig = plot_single_ccdf_degrees(degree,
                                           fit=f,
                                           name=name,
                                           figsize=figsize,
                                           ax=axs[i][j])

    return fig


def plot_single_edge_weight_distribution(edge_weights, name='untitled', ax=None, log=True, figsize=(5, 5)):
    if ax == None:
        fig, ax = plt.subplots(figsize=figsize)
    sns.set_context(rc={'patch.linewidth': 0.0});

    sns.histplot(edge_weights, bins=20, kde=True, log_scale=log, ax=ax);
    ax.set(xlabel='Edge Weights', ylabel='Frequency')
    ax.set(
        title=f"Edge Weight Distribution of\n{name.replace('_', ' ').title()}")

    return ax


def plot_edge_weight_distributions(*edge_weights, names=None, log=True, figsize=(5, 5)):
    if names == None:
        names = ['Unnamed' for _ in range(len(edge_weights))]
    if type(log) == bool:
        log = [log]

    # initialising subplots figure
    n_rows = len(edge_weights)
    n_cols = len(log)

    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(
        figsize[0]*n_cols, figsize[1]*n_rows), constrained_layout=True)

    # formatting axes array
    axs = np.array(axs)
    if n_rows > 1 and n_cols == 1:
        axs = axs.reshape(-1, 1)
    elif n_rows == 1 and n_cols > 1:
        axs = axs.reshape(1, -1)
    elif n_rows == 1 and n_cols == 1:
        axs = axs.reshape(1, 1)

    for i, edge_weight, name in zip(range(n_rows), edge_weights, names):
        for j, l in zip(range(n_cols), log):
            fig = plot_single_edge_weight_distribution(edge_weight,
                                                       name=name,
                                                       ax=axs[i][j],
                                                       log=l)

    return fig


def generate_plots(G, name, filepath='.', create_path=True):
    if create_path:
        os.makedirs(filepath) if not os.path.exists(filepath) else None

    names = ['degree_distribution',
             'ccdf_degree_distribution', 'edge_weight_distribution']
    funcs = [plot_degree_distribution, plot_ccdfs_degrees,
             plot_edge_weight_distributions]

    degrees = metrics.get_degrees(G)
    edge_weights = metrics.get_edge_weights(G)

    for func_name, func in zip(names, funcs):
        if func_name == 'degree_distribution':
            fig = func(degrees, names=[name], scales=['linear', 'log'])
        elif func_name == 'ccdf_degree_distribution':
            fig = func(degrees, names=[name], fit=[False, True])
        elif func_name == 'edge_weight_distribution':
            try:
                fig = func(edge_weights, name=name, log=True)
            except:
                None

        plt.savefig(f'{filepath}/{func_name}.jpg')


if __name__ == '__main__':
    # test code
    start = time()
    G = nx.read_gpickle('../data/projections/pickle_format/jaccard.pickle')
    print('finished loading in ' + str(time() - start))
    # G = nx.read_edgelist(f"../data/transformed/data.txt", delimiter=",", comments='#', create_using=nx.Graph)
    #degrees = [G.degree(node) for node in G.nodes() if node[0]=='r']
    #G2 = nx.read_gpickle('../data/projections/pickle_format/heats.pickle')

    #G = nx.karate_club_graph()
    #G2 = nx.karate_club_graph()

    start = time()
    edge_weights = metrics.get_edge_weights(G)
    #edge_weights = [edge[-1]['weight'] for edge in G.edges(data=True)]
    print('finished computing edge weights in ' + str(time() - start))
    # print(np.unique(edge_weights))

    #fig = plot_degree_distribution(degrees, degrees2, names=['test1', 'test2'], scales=['linear', 'log'])
    #fig = plot_ccdfs_degrees(metrics.get_degrees(G), fit=[False, True])
    fig = plot_edge_weight_distributions(
        edge_weights, names=['Jaccard'], log=[False, True])
    plt.show()
