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

def applyGeneticOperator(population, k, cProb, mProb):

	#	Select parents through a tournament of size k
	n_tournaments = 2
	parents = selectParents(population, k, n_tournaments)

	#	Cross parents with a probability cProb
	#		if random.randint(1,100) <= cProb:
	#			[1, 2, 3, 4]
	#			[5, 6, 7, 8]
	#if random.randint(1, 100) <= cProb:
	crossed_parents = crossParents(parents)

	#	Mutate parents with a probability mProb
	#		if random.randint(1,100) <= mProb:
	#			[1, 2, 7, 8] --> [3, 2, 7, 8]

	return population #Return the new population (not evaluated)

						#########################
						#	Auxiliar functions	#
						#########################

#	Gets the best solution from the "K" selected in a population.
def getKBestPrices(population, k):
	k_best_solutions = []
	for i in range(k):
		k_best_solutions.append(random.choice(population))

	k_best_solutions.sort(reverse = True)

	return k_best_solutions[1]

#	Selects "n_tournament" parents.
def selectParents(population, k, n_tournaments):
	parents = []
	for i in range(n_tournaments):
		parents.append(getKBestPrices(population, k))

	return parents

def crossParents(parents):
	print("parents:\t", parents)
	print("parents[0]:\t", parents[0])
	print("parents[0][0]:\t", parents[0][0])
	print("parents[0][0][0]:", parents[0][0][0])

	aux_parents = parents.copy()
	for i in range( int(len(parents[0][0]) / 2) ):
		aux_parents[0][0][i] = aux_parents[1][0][i]
		aux_parents[1][0][i] = aux_parents[0][0][i]

	print("aux_parents:", aux_parents)
						#########################

def main():
	#	Price/Weight
	weights = [ 34, 45, 14, 76, 32 ]
	prices = [ 340, 210, 87, 533, 112 ]
	maxWeight = 100 #Max weight in the knapsack.
	nSolutions = 20 #Population size [20 - 50].
	maxGenerations = 2 #Number of generations/iterations [100 - 300].
	k = 3 #Tournament selector size.
	cProb = 0.7 #Cross probability.
	mProb = 0.1 #Mutation probability.

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
	while it < maxGenerations:
		nSolutions = applyGeneticOperator(population, k, cProb, mProb)
		#Generational model
		population = []
		for solution in nSolutions:
			population.append([solution[0],evaluateSolution(solution[0], prices, weights, maxWeight)])
		it+=1

if __name__ == "__main__":
	main()
