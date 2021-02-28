import random
from client import *
import numpy as np

# overfit_file = open("overfit.txt", "r")
# initial_population = overfit_file.read()

initial_population = [0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11,
                      -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,
                      2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]

pop_size = 11

# train_error, validation_error = 13510723304.19212, 368296592820.6967

def fitness(error1, error2):
    return 1/(error1 + error2)

def mutation(population):
    mutation_factor = random.uniform(-1, 1)
    return [random.choice([i, i*mutation_factor]) for i in population]

def crossover(parent1, parent2):
    length1 = int(len(parent1)/2)
    length2 = int(len(parent2)/2)

    crossedParent1 = parent1[:length1] + parent2[length2:]
    crossedParent2 = parent1[length1:] + parent2[:length2]

    return crossedParent1, crossedParent2

generation = 0
fitness_pop = np.zeroes(pop_size)
prob_pop = np.zeroes(pop_size)
parents = np.zeroes(pop_size)
parents = np.copy(initial_population)
fertile_parents = np.zeroes(pop_size)

children = np.zeroes(pop_size)

colonization = []
colonization_fitness = []

while generation < 10:

    colonization.append(parents)

    errors = get_errors(SECRET_KEY, parents)
    print("GENERATION: ", generation)
    print("PARENTS: ", parents)
    print("ERRORS: ", errors)

    for i in range(pop_size):
        fitness_pop[i] = fitness(errors[i][0], errors[i][1])
        total_err = np.sum(fitness_pop)
        prob_pop[i] = (fitness_pop[i]/total_err)

    colonization_fitness.append(fitness_pop)

    fertile_parents = np.choice(parents, pop_size, p=prob_pop)

    print("FERTILE PARENTS: ", fertile_parents)

    mate_count = 0

    while mate_count < 10:
        offspring1, offspring2 = crossover(fertile_parents[mate_count], fertile_parents[mate_count+1])
        parents[mate_count] = offspring1
        parents[mate_count+1] = offspring2
        mate_count += 2

    offspring1, offspring2 = crossover(fertile_parents[0], fertile_parents[10])
    parents[10] = offspring1

    generation += 1

    print("====================================================")










#Continue mutating and crossing over the individual for some iterations
#Change the fitness, mutation and crossover functions according to the errors received
