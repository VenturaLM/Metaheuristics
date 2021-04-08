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

def applyGeneticOperator(population, k, cProb, mProb, prices, weights, maxWeight, elite):
	new_population = population.copy()
	#printPopulation(new_population)
	print("At the beginning:", elite)
	#	Select parents through a tournament of size k
	n_tournaments = 2
	parents = selectParents(population, k, n_tournaments)

	#	ELITE pre-operated, either crossed or muted. --> No se guarda el valor en las siguientes iteraciones.
	parents.sort(key = sortByProfit, reverse = True)
	if len(elite) == 0:
		elite = parents[0].copy()
	else:
		if elite[0][1] < parents[0][1]:
			elite = parents[0].copy()
	print("Elite:", elite)

	removeOldParentsFromPopulation(new_population, parents)
	#printPopulation(new_population)

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

	parents = updateOldPrice(parents, prices, weights, maxWeight)

	addNewParentsToPopulation(new_population, parents)

	#printPopulation(new_population)
	#	Return the new population (not evaluated) --> NOTA: En ocasiones al eliminar y añadir, el numero resultante de la poblacion final es distinto al de la inicial --> ¿Utilizar diccionario para contar cuantas veces se elimina cada uno?
	return new_population

						#########################
						#	Auxiliar functions	#
						#########################

#	Prints a population.
def printPopulation(population):
	for i in population:
		print(i)
	print("Population lenght:", len(population))
	print("\n")

#	Gets the best solution from the "K" selected in a population.
def getKBestPrices(population, k):
	k_best_solutions = []
	for i in range(k):
		k_best_solutions.append(random.choice(population))

	k_best_solutions.sort(key = sortByProfit, reverse = True)

	return k_best_solutions[1]

#	Sorting handling function.
def sortByProfit(k_best_solutions):
	return k_best_solutions[1]

#	Selects "n_tournament" parents.
def selectParents(population, k, n_tournaments):
	parents = []
	for i in range(n_tournaments):
		parents.append(getKBestPrices(population, k))

	return parents

#	Removes old parents from population.
def removeOldParentsFromPopulation(new_population, parents):
	for i in new_population:
		for j in parents:
			if i == j:
				new_population.remove(i)

#	Adds new parents to population.
def addNewParentsToPopulation(new_population, parents):
	for i in parents:
		new_population.append(i)

#	Crosses 2 parents.
#	Notas:
#		- En caso de que no sean 2 parents, si no varios en la estructura --> Corregir índices.
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
		print("MAIN:", elite)
		nSolutions = applyGeneticOperator(population, k, cProb, mProb, prices, weights, maxWeight, elite)
		#Generational model
		population = []
		for solution in nSolutions:
			population.append([solution[0], evaluateSolution(solution[0], prices, weights, maxWeight)])
		it+=1

if __name__ == "__main__":
	main()
