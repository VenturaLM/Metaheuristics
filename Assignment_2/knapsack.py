import random
import copy
import time
import os
import errno
import pandas as pd
import numpy as np


def evaluateSolution(solution, prices, weights, maxWeight):
    price = 0
    weight = 0
    for i in range(len(solution)):
        price += prices[i]*solution[i]
        weight += weights[i]*solution[i]

    if weight > maxWeight:
        return 0
    else:
        return price


def applyGeneticOperator(population, k, cProb, mProb, prices, weights, maxWeight):

    new_population = []
    parents = []

    while len(new_population) != len(population):

        #	Select parents through a tournament of size k
        parents = select2Parents(population, k).copy()

        #	Cross parents with a probability cProb
        #		if random.randint(1,100) <= cProb * 100:
        #			Example:
        #			[1, 2, 3, 4] & [5, 6, 7, 8] -->	[1, 2, 7, 8]

        if random.randint(1, 100) <= cProb * 100:
            parents = crossParents(parents).copy()

        #	Mutate parents with a probability mProb
        #		if random.randint(1,100) <= mProb:
        #			Example:
        #			[1, 2, 7, 8] --> [3, 2, 7, 8]

        if random.randint(1, 100) <= mProb * 100:
            parents = mutateParents(parents).copy()

        #	Evaluates parents prices. Sorts parents in order to get the best one. Then, the parent is appended to the "new_population".
        parents = updateOldPrice(parents, prices, weights, maxWeight)
        parents.sort(key=sortPopulationByProfit, reverse=True)

        for i in range(len(parents)):
            new_population.append(parents[i])

    #	Return the new population (not evaluated)
    return new_population

    #########################
    #	Auxiliar functions	#
    #########################


def printPopulation(p):
    #	Prints a population.
    for i in p:
        print(i)
    # print("Population lenght:", len(p))
    # print("\n")


def getKBestPrices(population, k):
    #	Gets the best solution from the "K" selected in a population.
    k_best_solutions = []
    for i in range(k):
        k_best_solutions.append(random.choice(population))

    k_best_solutions.sort(key=sortPopulationByProfit, reverse=True)

    return k_best_solutions[1]


def sortPopulationByProfit(p):
    #	Sorting handling function.
    return p[1]


def select2Parents(population, k):
    #	Selects 2 parents.
    aux_parents = []
    for i in range(2):
        aux_parents.append(getKBestPrices(population, k))

    return aux_parents


def crossParents(parents):
    #	Crosses 2 parents.
    aux_parents = copy.deepcopy(parents)
    for i in range(int(len(parents[0][0]) / 2)):
        aux_parents[0][0][i] = parents[1][0][i]
        aux_parents[1][0][i] = parents[0][0][i]

    return aux_parents


def mutateParents(parents):
    #	Mutates a random element from parents.
    aux_parents = copy.deepcopy(parents)
    for i in range(len(parents)):
        index = random.randint(0, 1)
        if aux_parents[i][0][index] == 0:
            aux_parents[i][0][index] = 1
        else:
            aux_parents[i][0][index] = 0

    return aux_parents


def updateOldPrice(parents, prices, weights, maxWeight):
    #	Updates old price.
    for i in range(len(parents)):
        parents[i][1] = evaluateSolution(
            parents[i][0], prices, weights, maxWeight)

    return parents


def printParentInfo(parents):
    #	Prints parents information.
    print("parents:\t", parents)
    print("parents[0]:\t", parents[0])
    print("parents[0][0]:\t", parents[0][0])
    print("parents[0][0][0]:", parents[0][0][0])


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

    #########################


def main():
    encoding = input(
        "Select type of encoding:\n1. Binary encoding. [Default]\n2. Integer enconding.\n> ")
    howManyTimesDoYouWannaRunThis = int(input("\nIterations:\n> "))

####################################################################################
    use_dataset = int(input(
        "\nDo you want to use any dataset?\n0. Default.\n1-25. Dataset size = 5.\n> "))

    dictionary = {'Elite': [], 'Seconds': [], 'Best_Solution': []}

    if use_dataset == 0:
        weights = [34, 45, 14, 76, 32]
        prices = [340, 210, 87, 533, 112]
    else:
        weights = []
        prices = []

        with open("./datasets/weights/dataset_" + str(use_dataset) + ".txt", "r") as filehandle:
            for line in filehandle:
                # Removes linebreak which is the last character of the string.
                currentPlace = line[:-1]

                weights = list(
                    map(int, currentPlace.strip('][').split(', '))).copy()

        with open("./datasets/prices/dataset_" + str(use_dataset) + ".txt", "r") as filehandle:
            for line in filehandle:
                # Removes linebreak which is the last character of the string.
                currentPlace = line[:-1]

                prices = list(
                    map(int, currentPlace.strip('][').split(', '))).copy()
####################################################################################
    for iterations in range(howManyTimesDoYouWannaRunThis):
        # Max weight in the knapsack.
        #   Note: Always maxWeight = sum(weights).
        maxWeight = 100
        if maxWeight > sum(weights):
            maxWeight = sum(weights)

        # Population size [20 - 50].
        #   Note: Even number.
        nSolutions = 20
        if nSolutions % 2 != 0:
            nSolutions += 1

        # Number of generations [100 - 300].
        maxGenerations = 100

        # Tournament selector size.
        k = 3

        # Cross probability.
        cProb = 0.7

        # Mutation probability.
        #   Note: In order to avoid randomness -->  [mProb <= 0.2].
        mProb = 0.1

        # Elite threshold will be the 25% of the population size.
        #   Note: In case [elite_threshold > 5] --> elite_threshold = 5.
        elite_threshold = int(nSolutions * 25 / 100)
        if elite_threshold > 5:
            elite_threshold = 5

        start_time = time.time()

        l = len(weights)
        # n random valid solutions are created
        population = []
        for i in range(nSolutions):
            objects = list(range(l))
            solution = []
            weight = 0
            while weight < maxWeight:
                object = objects[random.randint(0, len(objects) - 1)]
                weight += weights[object]
                if weight <= maxWeight:
                    solution.append(object)
                    objects.remove(object)

            s = []
            for i in range(l):
                s.append(0)

            if encoding == "2":
                for i in solution:
                    s[i] = random.randint(0, 5)
            else:
                encoding = "1"
                for i in solution:
                    s[i] = 1

            population.append(
                [s, evaluateSolution(s, prices, weights, maxWeight)])

        elite = []

        it = 1
        while it <= maxGenerations:
            nSolutions = applyGeneticOperator(
                population, k, cProb, mProb, prices, weights, maxWeight)

            # Generational model.
            population = []
            for solution in nSolutions:
                population.append([solution[0], evaluateSolution(
                    solution[0], prices, weights, maxWeight)])
            it += 1

            population.sort(key=sortPopulationByProfit, reverse=True)

            # Appends the "elite_threshold" best parents of the population to the elite.
            for i in range(elite_threshold):
                elite.append(population[i])

            # Evaluates elite.
            elite = evaluateElite(elite, elite_threshold).copy()

        print("\nElite:")
        printPopulation(elite)

        seconds = (time.time() - start_time)
        print("\n%s seconds" % seconds)

        dictionary['Elite'].append(elite)
        dictionary['Seconds'].append(seconds)
        dictionary['Best_Solution'].append(elite[0][1])

    directory = ""
    if encoding == "1":
        directory = "binary_encoding_data"
        try:
            os.mkdir(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    else:
        directory = "integer_encoding_data"
        try:
            os.mkdir(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    save_data = int(
        input("\nDo you want to save the data?\n1. Yes.\n2. No.\n> "))
    if save_data == 1:
        file_name = input("\nFile name:\n> ")
        if use_dataset == 0:
            file_name = file_name + "_default.txt"
        else:
            file_name = file_name + "_dataset_" + str(use_dataset) + ".txt"

        #	Creates the dataframe.
        df = pd.DataFrame(dictionary, columns=[
                          'Elite', 'Seconds', 'Best_Solution'])
        #	Change the context from "DataFrame" to "Numpy structure".
        numpy_array = df.to_numpy()
        #	Save the dataframe into a ".txt".
        np.savetxt("./" + directory + "/" + file_name,
                   numpy_array, fmt="%s", delimiter="\t")

        #	Checks if the file has been generated.
        try:
            if os.path.isfile("./" + directory + "/" + file_name):
                print(file_name, "generated.")
        except IOError:
            print("File not accessible.")


if __name__ == "__main__":
    main()
