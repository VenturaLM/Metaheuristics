import random
import time
import os
import errno
import pandas as pd
import numpy as np

def evaluateSolution(data, solution):
	routeLength = 0
	for i in range(len(solution)):
		routeLength += data[solution[i - 1]][solution[i]]
	return routeLength

def getBestNeighbor(solution, data):
	##Get the neighbors
	neighbors = []
	l=len(solution)
	for i in range(l):
		for j in range(i+1, l):
			n = solution.copy()
			n[i] = solution[j]
			n[j] = solution[i]
			neighbors.append(n)

	##Get the best neighbor
	bestNeighbor = neighbors[0]
	bestLength = evaluateSolution(data, bestNeighbor)
	for neighbor in neighbors:
		routeLength = evaluateSolution(data, neighbor)
		if routeLength < bestLength:
			bestLength = routeLength
			bestNeighbor = neighbor
	return bestNeighbor, bestLength

def generator(nCities):
	tsp = []
	for i in range(nCities):
		distances = []
		for j in range(nCities):
			if j == i:
				distances.append(0)
			elif j < i:
				distances.append(tsp[j][i])
			else:
				distances.append(random.randint(10, 1000))
		tsp.append(distances)
	return tsp

def hillClimbing(data):
	l=len(data)
	##Create a random solution
	cities = list(range(l))
	solution = []
	for i in range(l):
		city = cities[random.randint(0, len(cities) - 1)]
		solution.append(city)
		cities.remove(city)
	routeLength = evaluateSolution(data, solution)

	i = 1;
	print("Route length", i, ":", routeLength)
	##Get the best neighbor till no better neighbors can be obtained
	neighbor = getBestNeighbor(solution, data)
	while neighbor[1] < routeLength:
		solution = neighbor[0]
		routeLength = neighbor[1]
		i += 1;
		print("Route length", i, ":", routeLength)
		neighbor = getBestNeighbor(solution, data)

	return solution, routeLength

def main():

	#data = [
	#   [0, 400, 500, 300],
	#    [400, 0, 300, 500],
	#    [500, 300, 0, 400],
	#    [300, 500, 400, 0]
	#]
	print("\nFile to save the data:\n")
	file_name = input()

	minimum_cities = 10
	maximum_cities = 50
	increase = 10
	directory = "hill_climbing_data"

	dictionary = {'Cities': [], 'Seconds': []}

	for cities in range(minimum_cities , maximum_cities + increase, increase):
		print("\nCITIES =", cities)
		data = generator(cities)

		start_time = time.time()
		s=hillClimbing(data)

		print("--------------")
		seconds = (time.time() - start_time)

		print("%s seconds" % seconds)
		print("Final solution: ",s[0], "\n")
		print("Final route length: ",s[1], "\n")

		#	Creates "hill_climbing_data" directory
		try:
			os.mkdir(directory)

		except OSError as e:
			if e.errno != errno.EEXIST:
				raise

		dictionary['Cities'].append(cities)
		dictionary['Seconds'].append(seconds)

	#	Creates the dataframe.
	df = pd.DataFrame(dictionary, columns = ['Cities', 'Seconds'])
	#	Change the context from "DataFrame" to "Numpy structure".
	numpy_array = df.to_numpy()
	#	Save the dataframe in a ".txt".
	np.savetxt("./" + directory + "/" + file_name, numpy_array, fmt="%s")

	#	Checks if the file has been generated.
	try:
		if os.path.isfile("./" + directory + "/" + file_name):
			print(file_name, "generated.")
	except IOError:
		print("File not accessible.")

if __name__ == "__main__":
	main()
