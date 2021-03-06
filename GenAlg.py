import random
import matplotlib.pyplot as plt

one_Max_Length = 100

population_Size = 200
p_Crossover = 0.9
p_Mutation = 0.1
max_Generations = 50


class FitnessMax():
    def __init__(self):
        self.values = [0]


class Individual(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = FitnessMax()


def oneMaxFitness(individual):
    return sum(individual)


def individualCreator():
    return Individual([random.randint(0, 1) for i in range(one_Max_Length)])


def populationCreator(n=0):
    return list([individualCreator() for i in range(n)])


population = populationCreator(n=population_Size)
generationCounter = 0

fitnessValues = list(map(oneMaxFitness, population))

for individual, fitnessValues in zip(population, fitnessValues):
    individual.fitness.values = fitnessValues

maxFintessValues = []
meanFitnessValues = []


def clone(value):
    ind = Individual(value[:])
    ind.fitness.values = value.fitness.values
    return ind


def selTournament(population, p_len):
    offspring = []
    for n in range(p_len):
        i1 = i2 = i3 = 0
        while i1 == i2 or i1 == i3 or i2 == i3:
            i1, i2, i3 = random.randint(
                0, p_len-1), random.randint(0, p_len-1), random.randint(0, p_len-1)

        offspring.append(max([population[i1], population[i2],
                         population[i3]], key=lambda ind: ind.fitness.values))

    return offspring


def cxOnePoint(child1, child2):
    s = random.randint(2, len(child1)-3)
    child1[s:], child2[s:] = child2[s:], child1[s:]


def mutFlipBit(mutant, indpb=0.01):
    for indx in range(len(mutant)):
        if random.random() < indpb:
            mutant[indx] = 0 if mutant[indx] == 1 else 1


fitnessValues = [individual.fitness.values for individual in population]

while max(fitnessValues) < one_Max_Length and generationCounter < max_Generations:
    generationCounter += 1
    offspring = selTournament(population, len(population))
    offspring = list(map(clone, offspring))

    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < p_Crossover:
            cxOnePoint(child1, child2)

    for mutant in offspring:
        if random.random() < p_Mutation:
            mutFlipBit(mutant, indpb=1.0/one_Max_Length)

    freshFitnessValues = list(map(oneMaxFitness, offspring))
    for individual, fitnessValue in zip(offspring, freshFitnessValues):
        individual.fitness.values = fitnessValue

    population[:] = offspring

    fitnessValues = [ind.fitness.values for ind in population]

    maxFitness = max(fitnessValues)
    meanFitness = sum(fitnessValues) / len(population)
    maxFintessValues.append(maxFitness)
    meanFitnessValues.append(meanFitness)
    print(
        f'?????????????????? {generationCounter}: ???????? ??????????????????. = {maxFitness}, ?????????????? ??????????????????. = {meanFitness}')

    best_index = fitnessValues.index(max(fitnessValues))
    print('???????????? ???????????????????? = ', *population[best_index], '\n')

plt.plot(maxFintessValues, color='red')
plt.plot(meanFitnessValues, color='green')
plt.xlabel('??????????????????')
plt.ylabel('????????/?????????????? ??????????????????????????????????')
plt.title('?????????????????????? ???????????????????????? ?? ?????????????? ?????????????????????????????????? ???? ??????????????????')
plt.show()
