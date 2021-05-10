import matplotlib.pyplot as plt
from collections import defaultdict
import networkx as nx  # https://networkx.org/documentation/stable/index.html
import random
import numpy as np


def evaluateGraph(df, constraint):
    c = constraint.copy()

    # Evaluates if a graph is valid with a certain constraints.
    successful_records_indexes = []

    for i in range(len(df)):
        counter = 0
        target = len(df['Event'][i]) - 1
        for j in range(len(df['Event'][i])):
            if j + 1 < len(df['Event'][i]):
                if c[df['Event'][i][j] + df['Event'][i][j + 1]] != []:
                    # Checks that the current event satisfies the range constraint.
                    if (int(c[df['Event'][i][j] + df['Event'][i][j + 1]][0][0]) <= int(df['Time'][i][j])) and (int(c[df['Event'][i][j] + df['Event'][i][j + 1]][0][1]) >= int(df['Time'][i][j + 1])):
                        counter += 1

        if counter >= 1 and counter <= target:
            successful_records_indexes.append(i)

    return successful_records_indexes


def obtainConstraints(df, nConstraints, nSolutions):
    # Obtains "nSolutions" constraints.
    iterations = 0
    while iterations < nSolutions:
        constraint = defaultdict(list)
        index = random.randint(0, len(df['Event']) - 1)

        for i in range(len(df['Event'][index])):
            if i + 1 < len(df['Event'][index]):
                if constraint[df['Event'][index][i] + df['Event'][index][i + 1]].count([df['Time'][index][i], df['Time'][index][i + 1]]) < 1:
                    constraint[df['Event'][index][i] + df['Event'][index][i + 1]
                               ].append([df['Time'][index][i], df['Time'][index][i + 1]])

        nConstraints.append(constraint)
        iterations += 1


def plotSolutions(graph, graph_number):
    keys = list(graph.keys())
    values = list(graph.values())

    G = nx.Graph()
    labels = {}

    j = 0
    for i in keys:
        G.add_edge(i[0], i[1])
        labels[i[0] + i[1]] = values[j][0]
        j += 1

    edge_list = [(u, v) for (u, v, d) in G.edges(data=True)]

    # Position for all nodes.
    pos = nx.spring_layout(G)

    # Nodes.
    nx.draw_networkx_nodes(G, pos, node_size=250)

    # Edges.
    nx.draw_networkx_edges(G, pos, edgelist=edge_list, width=1)

    # Labels.
    nx.draw_networkx_labels(G, pos, font_size=12,
                            font_family="sans-serif")
    nx.draw_networkx_edge_labels(
        G, pos, verticalalignment="top", edge_labels=labels, font_size=10, font_family="sans-serif")

    plt.title("Solution " + str(graph_number))

    plt.axis("off")
    plt.show()
