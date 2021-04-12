import random
import copy


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

        # print("Elite 0:", elite)
        if random.randint(1, 100) <= cProb * 100:
            parents = crossParents(parents).copy()

        # print("Elite 1:", elite)
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
    print("Population lenght:", len(p))
    print("\n")


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


def evaluateElite(elite):
    #	Evaluate the current elite.
    elite.sort(key=sortPopulationByProfit, reverse=True)
    for i in range(5):
        #	Pops the last element until we got the limit.
        if len(elite) > 5:
            elite.pop(-1)

    return elite
    #########################


def main():
    #	Price/Weight
    weights = [34, 45, 14, 76, 32]
    prices = [340, 210, 87, 533, 112]
    maxWeight = 100  # Max weight in the knapsack.
    nSolutions = 20  # Population size [20 - 50].
    maxGenerations = 5  # Number of generations/iterations [100 - 300].
    k = 3  # Tournament selector size.
    # cProb = 0.7 #Cross probability.
    cProb = 1
    # mProb = 0.1 #Mutation probability. (In order to avoid randomness -->  [mProb <= 0.2] ).
    mProb = 1

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
        for i in solution:
            s[i] = 1
        population.append([s, evaluateSolution(s, prices, weights, maxWeight)])

    it = 1
    elite = []

    while it <= maxGenerations:
        # Aqui no lo cambia.
        nSolutions = applyGeneticOperator(
            population, k, cProb, mProb, prices, weights, maxWeight)
        # Aqui lo cambia.

        # Generational model
        population = []
        for solution in nSolutions:
            population.append([solution[0], evaluateSolution(
                solution[0], prices, weights, maxWeight)])
        it += 1

        #	Prints the updated population.
        population.sort(key=sortPopulationByProfit, reverse=True)
        # printPopulation(population)

        #	Appends the n best parents of the population to the elite.
        if len(elite) == 0:
            print("Population[0]:", population[0])
            elite = population[0].copy()

        print("Elite:", elite)

        #	Evaluates elite.
        # if len(elite) > 5:
        #	elite = evaluateElite(elite)

        # print("Elite:")
        # printPopulation(elite)


if __name__ == "__main__":
    main()
