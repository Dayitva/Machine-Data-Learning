import random
from client import *
import datetime

# overfit_file = open("overfit.txt", "r")
# initial_population = overfit_file.read()

initial_population = [0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11,
                      -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,
                      2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]

pop_size = 11
pop_size2 = 10
# train_error, validation_error = [13510723304.19212, 368296592820.6967]

def fitness(error1, error2):
    return 1/(error1 + error2)

def mutation(population, probability, mutate_from, mutate_till):
    mutation_factor = random.uniform(mutate_from, mutate_till)
    return [np.random.choice([i, i*mutation_factor], p=[probability, 1-probability]) for i in population]

def crossover(parent1, parent2, probability, mutate_from, mutate_till):
    length1 = int(np.size(parent1)/2)
    length2 = int(np.size(parent2)/2)

    crossedParent1 = np.concatenate((parent1[:length1], parent2[length2:]))
    crossedParent2 = np.concatenate((parent1[length1:], parent2[:length2]))

    return mutation(crossedParent1, probability, mutate_from, mutate_till), mutation(crossedParent2, probability, mutate_from, mutate_till)

generation = 0
fitness_pop = np.zeros(pop_size2)
prob_pop = np.zeros(pop_size2)
parents = [0 for i in range(10)]

for i in range(10):
    parents[i] = np.copy(mutation(initial_population, 0.9, 0.9, 1.1))

fertile_parents = np.zeros(pop_size2)

children = np.zeros(pop_size2)

colonization = []
colonization_fitness = []

crossover_probability = 0.8

while generation < pop_size2:
    for i in range(pop_size2):

        colonization.append(parents[i])

        errors = get_errors(SECRET_KEY, parents[i].tolist())
        with open("logs.txt", "a", encoding="utf8") as text_file:
            print("GENERATION: ", generation, file=text_file)
            print("PARENTS: ", parents[i], file=text_file)
            print("ERRORS: ", errors, file=text_file)

        fitness_pop[i] = fitness(errors[0], errors[1])
        colonization_fitness.append(fitness_pop[i])

    for i in range(pop_size2):
        total_err = np.sum(fitness_pop)
        prob_pop[i] = (fitness_pop[i]/total_err)

    idx = [i for i in range(pop_size2)]
    fertile_parents_idx = np.random.choice(idx, pop_size2, p=prob_pop)

    for i in range(pop_size2):
        with open("logs.txt", "a", encoding="utf8") as text_file:
            print("FERTILE PARENTS: ", parents[fertile_parents_idx[i]], file=text_file)

    mate_count = 0

    while mate_count < 10:
        offspring1, offspring2 = crossover(parents[fertile_parents_idx[mate_count]], parents[fertile_parents_idx[mate_count+1]], crossover_probability, 0.9, 1.1)
        parents[mate_count] = offspring1
        parents[mate_count+1] = offspring2
        mate_count += 2

    offspring1, offspring2 = crossover(parents[fertile_parents_idx[0]], parents[fertile_parents_idx[9]])
    parents[9] = offspring1

    generation += 1

    with open("logs.txt", "a", encoding="utf8") as text_file:
        print("====================================================", file=text_file)

    crossover_probability -= 0.1

population = len(colonization_fitness)

max_idx = 0
alpha_fitness = colonization_fitness[max_idx]

for i in range(0, population):
    if alpha_fitness < colonization_fitness[i]:
        max_idx = i
        alpha_fitness = colonization_fitness[max_idx]

with open("logs.txt", "a", encoding="utf8") as text_file:
    print("THE ALPHA IS: ", colonization[max_idx], " with fitness ", alpha_fitness," as logged on ", datetime.datetime.now(), file=text_file)
    print("====================================================", file=text_file)






#Continue mutating and crossing over the individual for some iterations
#Change the fitness, mutation and crossover functions according to the errors received
