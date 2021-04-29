import sys
import numpy as np
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt

# Create graph: https://www.geeksforgeeks.org/generate-graph-using-dictionary-python/

# [rango inferior; rango superior]
# [el elemento i - summation(i - 1); resta desde origen hasta destino]


def importFromTXTFile(file_name, lines):
    # Import a data base from a ".txt" file to a list.
    file = open(file_name, "r")
    for i in file:
        currentPlace = i[:-1]
        currentPlace = currentPlace.replace(" ", "")
        currentPlace = currentPlace.split(":")
        lines.append(currentPlace)


def moveToRecords(data, lines):
    # Adds to the dictionary each pair "Event" - "Time".
    # Example: [['A0', 'B10', 'C21']]
    for i in range(len(lines)):
        e = []
        t = []
        for j in range(len(lines[i])):
            for k in range(len(lines[i][j])):

                # If the character is a letter, it is a event.
                if lines[i][j][k].isalpha():
                    e.append(lines[i][j][k])
                else:
                    # The rest of the characters of the list[i][j][k] is a number.
                    t.append(lines[i][j][1:])
                    break
        data['Event'].append(e)
        data['Time'].append(t)


def createDataFrame(data):
    # Creates the dataframe.
    df = pd.DataFrame(data, columns=['Event', 'Time'])
    # Change the context from "DataFrame" to "Numpy structure".
    # numpy_array = df.to_numpy()
    return df


def addEdge(graph, u, v):
    # Adds an edge to a graph.
    graph.append([u, v])


def generateEdges(graph):
    # Generates graph's edges.
    edges = []
    # for each node in graph
    for node in graph:
        # for each neighbour node of a single node
        for neighbour in graph[node]:
            # if edge exists then append
            edges.append((node, neighbour))
    return edges


def buildGraph(graph, data):
    # Builds a graph.
    for i in range(len(data)):
        if i + 1 == len(data) - 1:
            # Adds the last pair of nodes (n - 1).
            addEdge(graph, data[-2], data[i][-1])
            break
        else:
            # Adds the (n - 2) pair of nodes.
            addEdge(graph, data[i], data[i + 1])


"""def classifyRecords(df, classification):
    # Classifies unique "Time" values for each key "Event".
    for i in range(len(df)):
        for j in range(len(df['Event'][i])):
            if classification[df['Event'][i][j]].count(df['Time'][i][j]) < 1:
                classification[df['Event'][i][j]].append(df['Time'][i][j])"""


def obtainConstraint(df, constraint):
    # Classifies unique "Time" range for each pair key "Event" on the first record of the dataframe.
    for i in range(len(df['Event'][0])):
        if i + 1 < len(df['Event'][0]):
            if constraint[df['Event'][0][i] + df['Event'][0][i + 1]].count([df['Time'][0][i], df['Time'][0][i + 1]]) < 1:
                constraint[df['Event'][0][i] + df['Event'][0][i + 1]
                           ].append([df['Time'][0][i], df['Time'][0][i + 1]])


def classifyRecords(df, classification):
    # Classifies unique "Time" range for each pair key "Event".
    for i in range(len(df)):
        for j in range(len(df['Event'][i])):
            if j + 1 < len(df['Event'][i]):
                if classification[df['Event'][i][j] + df['Event'][i][j + 1]].count([df['Time'][i][j], df['Time'][i][j + 1]]) < 1:
                    classification[df['Event'][i][j] + df['Event'][i][j + 1]
                                   ].append([df['Time'][i][j], df['Time'][i][j + 1]])


def evaluateGraph(df, constraint):
    # Evaluates if a graph is valid for a certain constraints.
    successful_records = 0
    # Range (1, inf) because the first record is already checked.
    for i in range(1, len(df)):
        counter = 0
        target = len(df['Event'][i]) - 1
        for j in range(len(df['Event'][i])):
            if j + 1 < len(df['Event'][i]):
                if constraint[df['Event'][i][j] + df['Event'][i][j + 1]] != []:
                    counter += 1
        if counter == target:
            successful_records += 1

    return successful_records


def main():
    if len(sys.argv) == 2:
        records = {'Event': [], 'Time': []}
        lines = []
        classification = defaultdict(list)
        constraint = defaultdict(list)

        # Gets the data into "lines".
        importFromTXTFile(sys.argv[1], lines)
        # Splits among "Events" and "Times" and stores it in "records" dictionary.
        moveToRecords(records, lines)
        # Generates a dataframe with the previous data.
        records_df = createDataFrame(records)
        print("Dataframe:\n", records_df)
        print("\n")

        # Para generar un grafo aleatorio con extensión igual al máximo.
        """maximum = 0
        for i in range(len(records_df['Event'])):
            if len(records_df['Event'][i]) > maximum:
                maximum = len(records_df['Event'][i])
        print(maximum)"""

        obtainConstraint(records_df, constraint)
        print("Constraint:", constraint)
        #classifyRecords(records_df, classification)
        # print(classification)
##############################################
        # Generates the multiple graphs. NOTA: HACER LISTA DE GRAFOS Y ALMACENARLO EN DOS GRANDES, UNA PARA CADA TIPO.
        #G = []
        solutions = 0
        # for i in range(1, len(records_df)):
        #   events_graph = []
        #  times_graph = []

        #buildGraph(events_graph, records_df['Event'][i])
        #buildGraph(times_graph, records_df['Time'][i])

        # G.append(events_graph)
        # print("Events graph " + str(i) + ":", events_graph)
        # print("Times graph " + str(i) + ":", times_graph)

        solutions += evaluateGraph(records_df, constraint)
        # print(G)
        print(solutions)
##############################################

    else:
        print("Mistaken input!\nExample: python3 main.py <data_base>.txt")


if __name__ == "__main__":
    main()
