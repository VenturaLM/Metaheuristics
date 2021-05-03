import sys
import numpy as np
import pandas as pd
from collections import defaultdict
# import matplotlib.pyplot as plt


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


def obtainConstraints(df, constraint):
    # Classifies unique "Time" range for each pair key "Event" on the first record of the dataframe.
    for i in range(len(df['Event'][0])):
        if i + 1 < len(df['Event'][0]):
            if constraint[df['Event'][0][i] + df['Event'][0][i + 1]].count([df['Time'][0][i], df['Time'][0][i + 1]]) < 1:
                constraint[df['Event'][0][i] + df['Event'][0][i + 1]
                           ].append([df['Time'][0][i], df['Time'][0][i + 1]])


def evaluateGraph(df, constraint):
    # Evaluates if a graph is valid with a certain constraints.
    successful_records = 0
    # Range (1, inf) because the first record is already checked (it is the constraint).
    for i in range(1, len(df)):
        counter = 0
        target = len(df['Event'][i]) - 1
        for j in range(len(df['Event'][i])):
            if j + 1 < len(df['Event'][i]):
                if constraint[df['Event'][i][j] + df['Event'][i][j + 1]] != []:
                    # Checks that the current event satisfies the range constraint.
                    if (int(constraint[df['Event'][i][j] + df['Event'][i][j + 1]][0][0]) <= int(df['Time'][i][j])) and (int(constraint[df['Event'][i][j] + df['Event'][i][j + 1]][0][1]) >= int(df['Time'][i][j + 1])):
                        counter += 1
                else:
                    break
        if counter == target:
            successful_records += 1

    return successful_records


def main():
    if len(sys.argv) == 2:
        records = {'Event': [], 'Time': []}
        lines = []
        constraint = defaultdict(list)

        # Gets the data into "lines".
        importFromTXTFile(sys.argv[1], lines)
        # Splits among "Events" and "Times" and stores it in "records" dictionary.
        moveToRecords(records, lines)
        # Generates a dataframe with the previous data.
        records_df = createDataFrame(records)
        # print("Dataframe:\n", records_df)
        # print("\n")

        obtainConstraints(records_df, constraint)
        # print("Constraint:", constraint)

        solutions = 0

        solutions += evaluateGraph(records_df, constraint)
        print("Solutions:", solutions)

    else:
        print("Mistaken input!\nExample: python3 main.py <data_base>.txt")


if __name__ == "__main__":
    main()
