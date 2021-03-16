import random
from client import *
import datetime
import numpy as np

initial_population = [0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11,
                      -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,
                      2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]

# [train_error, validation_error] = [13510723304.19212, 368296592820.6967]

vector_length = 11
population_length = 30
mutation_probability = 0.272727

zero_vector = [0.0 for i in range(vector_length)]

def get_initial_population():
    first_population = [np.copy(zero_vector) for i in range(population_length)]

    for i in range(population_length):
        mutation_factor = random.uniform(0.95, 1.05)
        first_population[i] = np.copy([np.random.choice([i, i*mutation_factor], p=[1-mutation_probability, mutation_probability]) if abs(i * mutation_factor) < 10 else i for i in initial_population])

    return first_population

def fitness(error1, error2):
    return 1/((error1*0.7) + error2)

def mutation(population, probability, mutate_from, mutate_till):
    mutation_factor = random.uniform(mutate_from, mutate_till)
    return [np.random.choice([i, i*mutation_factor], p=[1-probability, probability]) if abs(i * mutation_factor) < 10 else i for i in population]

def crossover(parent1, parent2):
    child1 = np.zeros(vector_length)
    child2 = np.zeros(vector_length)

    u = random.uniform(0, 0.999999)
    n = 5

    if u < 0.5:
        beta = (2 * u)**(1/(n + 1))
    else:
        beta = (1/(2 * (1 - u)))**(1/(n + 1))

    parent1 = np.array(parent1)
    parent2 = np.array(parent2)
    
    child1 = (((1 + beta) * parent1) + ((1 - beta) * parent2))/2
    child2 = (((1 - beta) * parent1) + ((1 + beta) * parent2))/2

    with open("generations.txt", "a", encoding="utf8") as text_file:
        print(child1, file=text_file)
        print(child2, file=text_file)

    child1 = np.copy(mutation(child1, mutation_probability, 0.9, 1.1))
    child2 = np.copy(mutation(child2, mutation_probability, 0.9, 1.1))

    return child1, child2

fitness_pop = np.zeros(population_length)
prob_pop = np.zeros(population_length)

parents = get_initial_population()
fertile_parents = np.zeros(population_length)
children = np.zeros(population_length)

colonization = []
colonization_fitness = []

generation = 0

while generation < 15:

    with open("generations.txt", "a", encoding="utf8") as text_file:
        print("GENERATION: ", generation+1, file=text_file)
        print("", file=text_file)

    with open("generations.txt", "a", encoding="utf8") as text_file:
        print("INITIAL POPULATION: ", file=text_file)

    for i in range(population_length):
        colonization.append(parents[i])
        errors = get_errors(SECRET_KEY, parents[i].tolist())

        with open("generations.txt", "a", encoding="utf8") as text_file:
            print(parents[i], file=text_file)

        fitness_pop[i] = fitness(errors[0], errors[1])
        colonization_fitness.append(fitness_pop[i])

    with open("generations.txt", "a", encoding="utf8") as text_file:
        print("", file=text_file)
        print("AFTER SELECTION: ", file=text_file)

    np_fitness = np.copy(colonization_fitness)
    np_colonization = np.copy(colonization)

    population_length -= 2

    fertile_parents_idx = np_colonization[np.argsort(np_fitness)]
    fertile_parents_idx = fertile_parents_idx[-1*population_length:]

    for i in range(population_length):
        with open("generations.txt", "a", encoding="utf8") as text_file:
            print(fertile_parents_idx[i], file=text_file)

    mate_count = 0

    with open("generations.txt", "a", encoding="utf8") as text_file:
        print("", file=text_file)
        print("AFTER CROSSOVER: ", file=text_file)

    while mate_count < population_length:
        offspring1, offspring2 = crossover(fertile_parents_idx[mate_count], fertile_parents_idx[mate_count+1])
        parents[mate_count] = offspring1
        parents[mate_count+1] = offspring2
        mate_count += 2

    with open("generations.txt", "a", encoding="utf8") as text_file:
        print("", file=text_file)
        print("AFTER MUTATION: ", file=text_file)

    for i in range(population_length):
        with open("generations.txt", "a", encoding="utf8") as text_file:
            print(parents[i], file=text_file)

    generation += 1

    with open("generations.txt", "a", encoding="utf8") as text_file:
        print("====================================================", file=text_file)
    
sorted_fitness = np.argsort(np_fitness)

for i in sorted_fitness[::-1][:10]:
    with open("output.txt", "a", encoding="utf8") as text_file:
        print(np_colonization[i].tolist(), file=text_file)