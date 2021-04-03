import random
import os
import errno

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

def main():
	directory = "datasets"
	cities = input("\nNumber of cities:\n>")
	tsp = generator(int(cities))
	"""for i in tsp:
		print(i)"""

	#   Creates "simulated_annealing_data" directory
	try:
		os.mkdir(directory)

	except OSError as e:
		if e.errno != errno.EEXIST:
			raise


	#file_name = input("\nFile to save the data:\n>")
	file_name = "dataset_" + str(cities) + "_cities.txt"

	with open("./" + directory + "/" + file_name, "w") as filehandle:
		filehandle.writelines("%s\n" % place for place in tsp)

	#   Checks if the file has been generated.
	try:
		if os.path.isfile("./" + directory + "/" + file_name):
			print("\n", file_name, "generated.")
	except IOError:
		print("File not accessible.")

if __name__ == "__main__":
	main()
