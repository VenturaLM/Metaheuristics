import random

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

	while len(new_population) != len(population):

		#	Select parents through a tournament of size k
		parents = select2Parents(population, k)

		#	Cross parents with a probability cProb
		#		if random.randint(1,100) <= cProb * 100:
		#			Example:
		#			[1, 2, 3, 4] & [5, 6, 7, 8] -->	[1, 2, 7, 8]

		if random.randint(1, 100) <= cProb * 100:
			parents = crossParents(parents)

		#	Mutate parents with a probability mProb
		#		if random.randint(1,100) <= mProb:
		#			Example:
		#			[1, 2, 7, 8] --> [3, 2, 7, 8]

		if random.randint(1, 100) <= mProb * 100:
			parents = mutateParents(parents)

		#	Evaluates parents prices. Sorts parents in order to get the best one. Then, the parent is appended to the "new_population".
		parents = updateOldPrice(parents, prices, weights, maxWeight)
		parents.sort(key = sortPopulationByProfit, reverse = True)
		new_population.append(parents[0])

		elite = parents[0].copy()

	#	Return the new population (not evaluated)
	return new_population

						#########################
						#	Auxiliar functions	#
						#########################

#	Prints a population.
def printPopulation(p):
	for i in p:
		print(i)
	print("Population lenght:", len(p))
	print("\n")

#	Gets the best solution from the "K" selected in a population.
def getKBestPrices(population, k):
	k_best_solutions = []
	for i in range(k):
		k_best_solutions.append(random.choice(population))

	k_best_solutions.sort(key = sortPopulationByProfit, reverse = True)

	return k_best_solutions[1]

#	Sorting handling function.
def sortPopulationByProfit(p):
	return p[1]

#	Selects "n_tournament" parents.
def select2Parents(population, k):
	parents = []
	for i in range(2):
		parents.append(getKBestPrices(population, k))

	return parents

#	Crosses 2 parents.
def crossParents(parents):
	aux_parents = parents.copy()
	for i in range( int(len(parents[0][0]) / 2) ):
		aux_parents[0][0][i] = aux_parents[1][0][i]
		aux_parents[1][0][i] = aux_parents[0][0][i]

	return aux_parents

#	Mutates a random element from parents.
def mutateParents(parents):
	aux_parents = parents.copy()
	for i in range( int(len(aux_parents)) ):
		if aux_parents[i][0][random.randint(0, 1)] == 0:
			aux_parents[i][0][random.randint(0, 1)] = 1
		else:
			aux_parents[i][0][random.randint(0, 1)] = 0

	return aux_parents

#	Updates old price.
def updateOldPrice(parents, prices, weights, maxWeight):
	for i in  range( int(len(parents)) ):
		parents[i][1] = evaluateSolution(parents[i][0], prices, weights, maxWeight)

	return parents

#	Prints parents information.
def printParentInfo(parents):
	print("parents:\t", parents)
	print("parents[0]:\t", parents[0])
	print("parents[0][0]:\t", parents[0][0])
	print("parents[0][0][0]:", parents[0][0][0])

#	Evaluate the current elite.
def evaluateElite(elite):
	elite.sort(key = sortPopulationByProfit, reverse = True)
	for i in range(5):
		#	Pops the last element.
		elite.pop(-1)

	return elite
						#########################

def main():
	#	Price/Weight
	weights = [ 34, 45, 14, 76, 32 ]
	prices = [ 340, 210, 87, 533, 112 ]
	maxWeight = 100 #Max weight in the knapsack.
	nSolutions = 20 #Population size [20 - 50].
	maxGenerations = 2 #Number of generations/iterations [100 - 300].
	k = 3 #Tournament selector size.
	#cProb = 0.7 #Cross probability.
	cProb = 1
	#mProb = 0.1 #Mutation probability.
	mProb = 1

	elite = []

	l=len(weights)
	##n random valid solutions are created
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

	it=1
	while it <= maxGenerations:
		nSolutions = applyGeneticOperator(population, k, cProb, mProb, prices, weights, maxWeight)

		#Generational model
		population = []
		for solution in nSolutions:
			population.append([solution[0], evaluateSolution(solution[0], prices, weights, maxWeight)])
		it+=1

		#	Prints the updated population.
		population.sort(key = sortPopulationByProfit, reverse = True)
		printPopulation(population)

		for i in range(5):
			elite.append(population[i])

		if len(elite) > 5:
			elite = evaluateElite(elite)

		print("Elite:")
		printPopulation(elite)

if __name__ == "__main__":
	main()
