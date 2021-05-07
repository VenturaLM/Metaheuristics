import sys
import copy
import pandas as pd
import time

import genetic_algorithm
import graph
import data_management

# Network graphs: https://www.youtube.com/watch?v=9aZiwuQTo-4


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
        data_management.importFromTXTFile(sys.argv[1], lines)

        # Splits among "Events" and "Times" and stores it in "records" dictionary.
        data_management.moveToRecords(records, lines)

        # Generates a dataframe with the previous data.
        records_df = data_management.createDataFrame(records)

        # Gets the length of the largest record. This will be used later in mutation.
        largest_record_length = data_management.getLargestRecords(
            records_df['Event'])

        # Gets a constraint similar to one of the records or generate new one.
        graph.obtainConstraints(records_df, nConstraints, nSolutions)
        # print("Constraints:", nConstraints)

        elite = []
        # Population will store --> [Indexes of solution / % of satisfaction / Graph]
        population = []
        elite_threshold = 5

        dictionary = {'Elite': [], 'Profit': [], 'Graph': []}

        start_time = time.time()

        for constraint in nConstraints:
            s = graph.evaluateGraph(records_df, constraint)

            # Appends into population --> indexes of the records that satisfy the constraints and the satisfaction percentage of the total elements.
            population.append([s, len(s)/len(records_df['Event']), constraint])

        # Selects the best parents of the very first population and saves them into elite.
        genetic_algorithm.selectElite(population, elite, elite_threshold)

        # Number of generations [100 - 300].
        maxGenerations = 1

        iterations = 1
        while iterations <= maxGenerations:
            nSolutions = genetic_algorithm.applyGeneticOperator(
                nConstraints, mProb, largest_record_length)

            # TODO: evaluateGraph --> PARA VER QUÉ RECORDS SATISFACEN LOS NUEVOS CONSTRAINTS.

            # TODO: CREAR OTRA VEZ POPULATION Y METERLE DE NUEVO LOS PARÁMETROS QUE TIENE ARRIBA.

            # Selects the best parents and saves them into elite.
            genetic_algorithm.selectElite(population, elite, elite_threshold)
            # Checks the elite and take the unique elements.
            elite = genetic_algorithm.evaluateElite(
                elite, elite_threshold).copy()

            iterations += 1

        seconds = (time.time() - start_time)

        # Saves elite into dictionary.
        genetic_algorithm.saveEliteIntoDictionary(dictionary, elite)

        # Creates elite dataframe.
        elite_df = pd.DataFrame(dictionary, columns=[
                                'Elite', 'Profit', 'Graph'])
        print(elite_df)

        print("\n%s seconds" % seconds)

    else:
        print("Mistaken input!\nExample: python3 main.py <data_base>.txt")


if __name__ == "__main__":
    main()
