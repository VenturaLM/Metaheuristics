import random
from TSPGenerator import generator
import time
import os
import errno
import pandas as pd
import numpy as np
import pickle

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

	directory = "iterated_hill_climbing_data"
	cities = input("\nNumber of cities:\n>")
	iterations = 5

	dictionary = {'Best_Solution': [], 'Seconds': []}

#############################################################

	data = []

	#	Generate random data:
	#data = generator(int(cities))

	#	Import your data from ".txt" file.
	with open("./datasets/dataset_" + str(cities) + "_cities.txt", "r") as filehandle:
		for line in filehandle:
			# remove linebreak which is the last character of the string
			currentPlace = line[:-1]

			# add item to the list
			data.append(list(map(int, currentPlace.strip('][').split(', '))))

#############################################################

	for i in range(iterations):
		print("\nITERATION =", i + 1)

		start_time = time.time()
		s=hillClimbing(data)

		print("--------------")
		seconds = (time.time() - start_time)

		print("%s seconds" % seconds)
		print("Final solution: ",s[0], "\n")
		print("Final route length: ",s[1], "\n")

		#	Creates "iterated_hill_climbing_data" directory
		try:
			os.mkdir(directory)

		except OSError as e:
			if e.errno != errno.EEXIST:
				raise

		dictionary['Best_Solution'].append(int(s[1]))
		dictionary['Seconds'].append(seconds)

	save_data = input("\nDo you want to save the data?\n1. Yes.\n2. No.\n>")
	if save_data == "1":
		file_name = "data_" + str(cities) + "_cities.txt"

		#	Creates the dataframe.
		df = pd.DataFrame(dictionary, columns = ['Best_Solution', 'Seconds'])
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
