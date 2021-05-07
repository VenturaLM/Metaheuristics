import sys
import copy
import numpy as np
import pandas as pd
from collections import defaultdict
import time
import random
import matplotlib.pyplot as plt

# Network graphs: https://www.youtube.com/watch?v=9aZiwuQTo-4


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


def mutation_1(constraint, largest_record_length):
    # Adds a new random event to the current constraint if the length of the current constraint is smaller than the maximum one on the data base.
    events = ['A', 'B', 'C', 'D', 'E']

    if len(constraint) < largest_record_length:
        keys = list(constraint.keys())
        values = list(constraint.values())
        # contraint[last_event + new_random_event].append([last_time, random_time(last_time, last_time + 10)])
        constraint[keys[-1][-1] + events[random.randint(0, 4)]].append([values[-1][0][1], random.randint(int(
            values[-1][0][1]), int(values[-1][0][1]) + 5)])


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


def sortPopulationByProfit(p):
    #	Sorting handling function.
    return p[1]


def evaluateElite(elite, elite_threshold):
    #	Evaluate the current elite.
    elite.sort(key=sortPopulationByProfit, reverse=True)
    counter = len(elite)
    i = 0

    while i < counter:
        j = i + 1
        while j < counter:
            if elite[i] == elite[j]:
                elite.pop(j)
                counter -= 1
                j -= 1
            j += 1
        i += 1

    while len(elite) > elite_threshold:
        elite.pop(-1)

    return elite


def saveEliteIntoDictionary(dictionary, elite):
    # Saves the current elite into dictionary data structure.
    for i in range(len(elite)):
        dictionary['Elite'].append(elite[i][0])
        dictionary['Profit'].append(elite[i][1])
        dictionary['Graph'].append(elite[i][2])


def selectElite(population, elite, elite_threshold):
    # Selects the best "elite_threshold" elements of the populations and stores it in "elite".
    population.sort(key=sortPopulationByProfit, reverse=True)

    for i in range(elite_threshold):
        elite.append(population[i])


def applyGeneticOperator(nConstraints, mProb, largest_record_length):
    # new_population will store --> [Indexes of solution / % of satisfaction / Graph]
    new_nConstraints = []
    parents = []

    while len(new_nConstraints) != len(nConstraints):
        #	Select 2 random parents from the population.
        parents = select2Parents(nConstraints).copy()

        #	Mutate parents with a probability mProb
        #		if random.randint(1,100) <= mProb:
        #			Example:
        #			[1, 2, 7, 8] --> [3, 2, 7, 8]
        if random.randint(1, 100) <= mProb * 100:
            # TODO: HACER LA FUNCION. ES JUSTAMENTE LO QUE ME TOCA AHORA!
            print("Mutation 1 applicated!")

        for i in range(len(parents)):
            new_nConstraints.append(parents[i])

    print(parents)

    return  # TODO: RETORNAR LA NUEVA POBLACION DE CONSTRAINTS


def select2Parents(p):
    #	Selects 2 parents.
    parents = []
    i = 0
    while i < 2:
        parents.append(random.choice(p))
        i += 1

    return parents


def main():
    if len(sys.argv) == 2:
        records = {'Event': [], 'Time': []}
        lines = []
        nConstraints = []

        # Population size [20 - 50].
        #   Note: Even number.
        nSolutions = 20
        if nSolutions % 2 != 0:
            nSolutions += 1

        # Mutation probability.
        #   Note: In order to avoid randomness -->  [mProb <= 0.2].
        mProb = 0.0

        # Gets the data into "lines".
        importFromTXTFile(sys.argv[1], lines)

        # Splits among "Events" and "Times" and stores it in "records" dictionary.
        moveToRecords(records, lines)

        # Generates a dataframe with the previous data.
        records_df = createDataFrame(records)

        # Gets the length of the largest record. This will be used later in mutation.
        largest_record_length = getLargestRecords(records_df['Event'])

        # Gets a constraint similar to one of the records or generate new one.
        obtainConstraints(records_df, nConstraints, nSolutions)
        # print("Constraints:", nConstraints)

        elite = []
        # Population will store --> [Indexes of solution / % of satisfaction / Graph]
        population = []
        elite_threshold = 5

        dictionary = {'Elite': [], 'Profit': [], 'Graph': []}

        start_time = time.time()

        for constraint in nConstraints:
            s = evaluateGraph(records_df, constraint)

            # Appends into population --> indexes of the records that satisfy the constraints and the satisfaction percentage of the total elements.
            population.append([s, len(s)/len(records_df['Event']), constraint])

        # Selects the best parents of the very first population and saves them into elite.
        selectElite(population, elite, elite_threshold)

        # Number of generations [100 - 300].
        maxGenerations = 1

        iterations = 1
        while iterations <= maxGenerations:
            nSolutions = applyGeneticOperator(
                nConstraints, mProb, largest_record_length)

            # TODO: evaluateGraph --> PARA VER QUÉ RECORDS SATISFACEN LOS NUEVOS CONSTRAINTS.

            # TODO: CREAR OTRA VEZ POPULATION Y METERLE DE NUEVO LOS PARÁMETROS QUE TIENE ARRIBA.

            # Selects the best parents and saves them into elite.
            selectElite(population, elite, elite_threshold)
            # Checks the elite and take the unique elements.
            elite = evaluateElite(elite, elite_threshold).copy()

            iterations += 1

        seconds = (time.time() - start_time)

        # Saves elite into dictionary.
        saveEliteIntoDictionary(dictionary, elite)

        # Creates elite dataframe.
        elite_df = pd.DataFrame(dictionary, columns=[
                                'Elite', 'Profit', 'Graph'])
        print(elite_df)

        print("\n%s seconds" % seconds)

    else:
        print("Mistaken input!\nExample: python3 main.py <data_base>.txt")


if __name__ == "__main__":
    main()
