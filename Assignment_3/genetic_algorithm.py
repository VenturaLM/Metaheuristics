import random
import copy


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

    if len(population) != 0:
        if len(population) < elite_threshold:
            elite_threshold = len(population)

        for i in range(elite_threshold):
            elite.append(population[i])

    return elite


def applyGeneticOperator(nConstraints, mProb, largest_record_length, elite):
    # new_population will store --> [Indexes of solution / % of satisfaction / Graph]
    new_nConstraints = []
    parents = []

    while len(new_nConstraints) != len(nConstraints):
        #	Select 2 random parents from the population.
        parents = select2Parents(nConstraints).copy()

        #	Mutate parents with a probability mProb
        #		if random.randint(1,100) <= mProb:
        #			Example:
        #			{'AB': [['1', '3']], 'BA': [['3', '4']]} --> {'BA': [['3', '4']], 'AA': [['1', '3']]}
        if random.randint(1, 100) <= mProb * 100:
            parents = mutateParentsGene(parents)
            parents = mutateParentsAddGene(parents, largest_record_length)

        for i in range(len(parents)):
            new_nConstraints.append(parents[i])

    return new_nConstraints


def mutateParentsAddGene(parents, largest_record_length):
    # Adds a new random event to the current constraint if the length of the current constraint is smaller than the maximum one on the data base.
    # NOTE: It is very important to use copy.deepcopy(). Somehow, data direction would be corrupted instead.
    p = copy.deepcopy(parents)
    events = ['A', 'B', 'C', 'D', 'E']

    for i in p:
        if len(i) < largest_record_length:
            keys = list(i.keys())
            values = list(i.values())
            # contraint[last_event + new_random_event].append([last_time, random_time(last_time, last_time + 10)])
            i[keys[-1][-1] + events[random.randint(0, 4)]].append([values[-1][0][1], random.randint(int(
                values[-1][0][1]), int(values[-1][0][1]) + 5)])

    return p


def mutateParentsGene(parents):
    # Mutate a random event gene from each parent.
    # NOTE: It is very important to use copy.deepcopy(). Somehow, data direction would be corrupted instead.
    p = copy.deepcopy(parents)
    events = ['A', 'B', 'C', 'D', 'E']
    to_mutate = events[random.randint(0, 4)]
    new_mutation = to_mutate

    while new_mutation == to_mutate:
        new_mutation = events[random.randint(0, 4)]

    for i in range(len(p)):
        for j in list(p[i].keys()):
            current_key = j
            if j[0] == to_mutate:
                new_key = new_mutation + j[1]
                if current_key in p[i]:
                    p[i][new_key] = p[i].pop(current_key)
                    current_key = new_key
            if j[1] == to_mutate:
                new_key = j[0] + new_mutation
                if current_key in p[i]:
                    p[i][new_key] = p[i].pop(current_key)

    return p


def select2Parents(p):
    #	Selects 2 parents.
    parents = []
    i = 0
    while i < 2:
        parents.append(random.choice(p))
        i += 1

    return parents
