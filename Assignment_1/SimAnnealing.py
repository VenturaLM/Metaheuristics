import random
import math
from TSPGenerator import generator
import time
import os
import errno
import pandas as pd
import numpy as np

def evaluateSolution(data, solution):
	lengthTravel = 0
	for i in range(len(solution)):
		lengthTravel += data[solution[i - 1]][solution[i]]
	return lengthTravel

def getNeighbor(solution, data):
	##Get the neighbors
	neighbors = []
	l=len(solution)
	for i in range(l):
		for j in range(i+1, l):
			n = solution.copy()
			n[i] = solution[j]
			n[j] = solution[i]
			neighbors.append(n)

	##Get a random neighbor
	neighbor=neighbors[random.randint(0, len(neighbors) - 1)]
	lengthTravel = evaluateSolution(data, neighbor)

	return neighbor, lengthTravel

def simAnnealing(data, t0, dictionary):
	t=t0
	l=len(data)
	##Generate a random solution
	start_time = time.time()	#	Starts the time counter.

	cities = list(range(l))
	solution = []
	for i in range(l):
		ciudad = cities[random.randint(0, len(cities) - 1)]
		solution.append(ciudad)
		cities.remove(ciudad)
	lengthTravel = evaluateSolution(data, solution)

	seconds = (time.time() - start_time)	#	Ends the time counter.

	print("Length of the route: ", lengthTravel)
	print("Temperature: ", t)

	dictionary['Best_Solution'].append(lengthTravel)
	dictionary['Seconds'].append(seconds)
	dictionary['Temperature'].append(t)

	it=0
	while t > 0.05:
		##Get a random neighbor
		start_time = time.time()	#	Starts the time counter.

		neighbor = getNeighbor(solution, data)
		increment = neighbor[1]-lengthTravel

		if increment < 0:
			lengthTravel = neighbor[1]
			solution = neighbor[0]
		elif random.random() < math.exp(-abs(increment) / t):
			lengthTravel = neighbor[1]
			solution = neighbor[0]

		it+=1
		t=0.99*t
		seconds = (time.time() - start_time)	#	Ends the time counter.

		print("Length of the route: ", lengthTravel)
		print("Temperature: ", t)

		dictionary['Best_Solution'].append(lengthTravel)
		dictionary['Seconds'].append(seconds)
		dictionary['Temperature'].append(t)

	return solution, lengthTravel

def main():

	directory = "simulated_annealing_data"
	subdirectory = directory + "/data_per_city"
	cities = input("\nNumber of cities:\n>")
	dictionary = {'Best_Solution': [], 'Seconds': [], 'Temperature': []}

#############################################################
	#	Copy and paste your own data:
	"""data = [
	   
	]"""

	#	Generate random data:
	data = generator(int(cities))

#############################################################

	t0=10

	s=simAnnealing(data, t0, dictionary)

	print("--------------")
	print("Final solution: ",s[0])
	print("Length of the final route: ",s[1])

	#	Creates "simulated_annealing_data" directory
	try:
		os.mkdir(directory)
		os.mkdir(subdirectory)

	except OSError as e:
		if e.errno != errno.EEXIST:
			raise

	save_data = input("\nDo you want to save the data?\n1. Yes.\n2. No.\n>")
	if save_data == "1":
		#file_name = input("\nFile to save the data:\n>")
		file_name = "data_" + str(cities) + "_cities.txt"

		#	Creates the dataframe.
		df = pd.DataFrame(dictionary, columns = ['Best_Solution', 'Seconds', 'Temperature'])
		#	Change the context from "DataFrame" to "Numpy structure".
		numpy_array = df.to_numpy()
		#	Save the dataframe in a ".txt".
		np.savetxt("./" + subdirectory + "/" + file_name, numpy_array, fmt="%s")

		#	Checks if the file has been generated.
		try:
			if os.path.isfile("./" + subdirectory + "/" + file_name):
				print("\n", file_name, "generated.")
		except IOError:
			print("File not accessible.")

if __name__ == "__main__":
	main()
