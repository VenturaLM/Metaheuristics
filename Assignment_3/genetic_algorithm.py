import random


def mutation_1(constraint, largest_record_length):
    # Adds a new random event to the current constraint if the length of the current constraint is smaller than the maximum one on the data base.
    events = ['A', 'B', 'C', 'D', 'E']

    if len(constraint) < largest_record_length:
        keys = list(constraint.keys())
        values = list(constraint.values())
        # contraint[last_event + new_random_event].append([last_time, random_time(last_time, last_time + 10)])
        constraint[keys[-1][-1] + events[random.randint(0, 4)]].append([values[-1][0][1], random.randint(int(
            values[-1][0][1]), int(values[-1][0][1]) + 5)])


def sortPopulationByProfit(p):
    #	Sorting handling function.
    return p[1]


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


def saveEliteIntoDictionary(dictionary, elite):
    # Saves the current elite into dictionary data structure.
    for i in range(len(elite)):
        dictionary['Elite'].append(elite[i][0])
        dictionary['Profit'].append(elite[i][1])
        dictionary['Graph'].append(elite[i][2])


def selectElite(population, elite, elite_threshold):
    # Selects the best "elite_threshold" elements of the populations and stores it in "elite".
    population.sort(key=sortPopulationByProfit, reverse=True)

    for i in range(elite_threshold):
        elite.append(population[i])


def applyGeneticOperator(nConstraints, mProb, largest_record_length):
    # new_population will store --> [Indexes of solution / % of satisfaction / Graph]
    new_nConstraints = []
    parents = []

    while len(new_nConstraints) != len(nConstraints):
        #	Select 2 random parents from the population.
        parents = select2Parents(nConstraints).copy()

        #	Mutate parents with a probability mProb
        #		if random.randint(1,100) <= mProb:
        #			Example:
        #			[1, 2, 7, 8] --> [3, 2, 7, 8]
        if random.randint(1, 100) <= mProb * 100:
            # TODO: HACER LA FUNCION. ES JUSTAMENTE LO QUE ME TOCA AHORA!
            print("Mutation 1 applicated!")

        for i in range(len(parents)):
            new_nConstraints.append(parents[i])

    print(parents)

    return  # TODO: RETORNAR LA NUEVA POBLACION DE CONSTRAINTS


def select2Parents(p):
    #	Selects 2 parents.
    parents = []
    i = 0
    while i < 2:
        parents.append(random.choice(p))
        i += 1

    return parents
