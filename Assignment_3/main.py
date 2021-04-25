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
    print(df)


def addEdge(graph, u, v):
    # Adds an edge to a graph.
    graph[u].append(v)


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
        for j in range(len(data[i])):
            if j + 1 == len(data[i]) - 1:
                # Adds the last pair of nodes (n - 1).
                addEdge(graph, data[i]
                        [-2], data[i][-1])
                break
            else:
                # Adds the (n - 2) pair of nodes.
                addEdge(graph, data[i][j],
                        data[i][j + 1])
    return generateEdges(graph)


def main():
    if len(sys.argv) == 2:
        records = {'Event': [], 'Time': []}
        lines = []
        # Clave - valor,: por ejemplo, a esta conectado con b y c en la impresion del defaultdict; eso no pasa con los numeros.
        eventsGraph = defaultdict(list)
        timesGraph = defaultdict(list)

        # Gets the data into "lines".
        importFromTXTFile(sys.argv[1], lines)
        # Splits among "Events" and "Times" and stores it in "records" dictionary.
        moveToRecords(records, lines)
        # Generates a dataframe with the previous data.
        createDataFrame(records)

        #e = buildGraph(eventsGraph, records['Event'])
        #t = buildGraph(timesGraph, records['Time'])

        #print("Events graph:", e)
        #print("Times graph:", t)

    else:
        print("Mistaken input!\nExample: python3 main.py <data_base>.txt")


if __name__ == "__main__":
    main()
