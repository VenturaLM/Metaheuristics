import matplotlib.pyplot as plt
from collections import defaultdict
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
                else:
                    break
        if counter == target:
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


def plotSolutions():
    x = np.linspace(0, 2, 100)

    plt.plot(x, x, label='linear')
    plt.plot(x, x**2, label='quadratic')
    plt.plot(x, x**3, label='cubic')
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.title("Simple Plot")
    plt.legend()

    plt.show()
