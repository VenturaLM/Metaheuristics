import random
import os
import errno


def weightsGenerator(nItems):
    weights = []
    for i in range(nItems):
        weights.append(random.randint(10, 200))

    return weights


def pricesGenerator(nItems):
    prices = []
    for i in range(nItems):
        prices.append(random.randint(10, 1000))

    return prices


def main():
    iterations = int(input("Amount of datasets:\n> "))
    items = int(input("\nItems in knapsack:\n> "))

    for i in range(iterations + 1):
        directory = "datasets"
        weights_directory = "weights"
        prices_directory = "prices"

        weights = []
        weights.append(weightsGenerator(items))

        prices = []
        prices.append(pricesGenerator(items))

        #   Creates directories:
        try:
            os.mkdir(directory)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        try:
            os.mkdir(directory + "/" + weights_directory)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        try:
            os.mkdir(directory + "/" + prices_directory)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

            # file_name = input("\nFile to save the data:\n> ")
            weights_file_name = "dataset_" + str(i) + ".txt"
            prices_file_name = "dataset_" + str(i) + ".txt"

            with open("./" + directory + "/" + weights_directory + "/" + weights_file_name, "w") as filehandle:
                filehandle.writelines("%s\n" % place for place in weights)

            with open("./" + directory + "/" + prices_directory + "/" + prices_file_name, "w") as filehandle:
                filehandle.writelines("%s" % place for place in prices)

            #   Checks if the file has been generated.
            try:
                if os.path.isfile("./" + directory + "/" + weights_directory + "/" + weights_file_name):
                    print(weights_file_name, "generated.")
            except IOError:
                print("File not accessible.")

            try:
                if os.path.isfile("./" + directory + "/" + prices_directory + "/" + prices_file_name):
                    print(prices_file_name, "generated.")
            except IOError:
                print("File not accessible.")


if __name__ == "__main__":
    main()
