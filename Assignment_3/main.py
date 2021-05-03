import sys
import numpy as np
import pandas as pd
from collections import defaultdict
import time
import random
import matplotlib.pyplot as plt


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
    # Gets a graph with, at least, 4 events, including its respective constraints.
    index = 0
    for i in range(len(df['Event'])):
        if len(df['Event'][index]) < 4:
            index += 1
        else:
            break

    for i in range(len(df['Event'][index])):
        if i + 1 < len(df['Event'][index]):
            if constraint[df['Event'][index][i] + df['Event'][index][i + 1]].count([df['Time'][index][i], df['Time'][index][i + 1]]) < 1:
                constraint[df['Event'][index][i] + df['Event'][index][i + 1]
                           ].append([df['Time'][index][i], df['Time'][index][i + 1]])


def evaluateGraph(df, constraint, mProb, largest_record_length):
    # Evaluates if a graph is valid with a certain constraints.
    successful_records_indexes = []
    partially_successful_record_indexes = []

    if random.randint(1, 100) <= mProb * 100:
        mutation_1(constraint, largest_record_length)

    for i in range(len(df)):
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
            successful_records_indexes.append(i)
        if counter == int(target/2):
            partially_successful_record_indexes.append(i)

    return successful_records_indexes, partially_successful_record_indexes


def mutation_1(constraint, largest_record_length):
    # Adds a new random event to the current constraint if the length of the current constraint is smaller than the maximum one on the data base.
    events = ['A', 'B', 'C', 'D', 'E']

    if len(constraint) < largest_record_length:
        keys = list(constraint.keys())
        values = list(constraint.values())
        # contraint[last_event + new_random_event].append([last_time, random_time(last_time, last_time + 10)])
        constraint[keys[-1][-1] + events[random.randint(0, 4)]].append([values[-1][0][1], random.randint(int(
            values[-1][0][1]) + 1, int(values[-1][0][1]) + 10)])


def printSolution(s):
    # Solutions including the one that matches with the constraint.
    print("\nSolutions that satisfy the [100%] of the constraint:", len(s[0]))
    # print("Indexes:", s[0])

    print("Solutions that satisfy [50% - 100%] of the constraint:", len(s[1]))
    # print("Indexes:", s[1])


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


def getLargestRecords(r):
    maximum = 0
    for i in range(len(r)):
        if len(r[i]) > maximum:
            maximum = len(r[i])
    return maximum


def main():
    # NOTA: CREO QUE NO ESTÁ BIEN DEL TODO, DEBIDO A QUE LOS RANGOS NO SON COMO EN EL EJEMPLO, DADO QUE YO NO CONTEMPLO NUMERO NEGATIVOS. ADEMÁS, PREGUNTAR SOBRE QUÉ HACER LA MUTACION, SI SOBRE EL RANGO O SOBRE LOS NODOS (EVENTOS).
    if len(sys.argv) == 2:
        records = {'Event': [], 'Time': []}
        lines = []
        constraint = defaultdict(list)
        mProb = 1

        # Gets the data into "lines".
        importFromTXTFile(sys.argv[1], lines)

        # Splits among "Events" and "Times" and stores it in "records" dictionary.
        moveToRecords(records, lines)

        # Generates a dataframe with the previous data.
        records_df = createDataFrame(records)

        # Gets the length of the largest record. This will be used later in mutation.
        largest_record_length = getLargestRecords(records_df['Event'])

        obtainConstraints(records_df, constraint)
        # print("Constraint:", constraint)

        start_time = time.time()
        s = evaluateGraph(records_df, constraint, mProb, largest_record_length)
        seconds = (time.time() - start_time)

        printSolution(s)
        print("\n%s seconds" % seconds)

    else:
        print("Mistaken input!\nExample: python3 main.py <data_base>.txt")


if __name__ == "__main__":
    main()
