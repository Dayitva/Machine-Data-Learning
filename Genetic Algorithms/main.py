import random
from client import *
import datetime

# overfit_file = open("overfit.txt", "r")
# initial_population = overfit_file.read()

initial_population = [0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11,
                      -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,
                      2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]

start_pop = [0.0 for i in range(11)]

pop_size = 11
pop_size2 = 10

# train_error, validation_error = [13510723304.19212, 368296592820.6967]

def fitness(error1, error2):
    return 1/((error1*0.7) + error2)

def mutation(population, probability, mutate_from, mutate_till):
    mutation_factor = random.uniform(mutate_from, mutate_till)
    return [np.random.choice([i, i*mutation_factor], p=[1-probability, probability]) if abs(i * mutation_factor) < 10 else i for i in population]

def get_initial_population():
    first_population = [np.copy(start_pop) for i in range(pop_size2)]
    
    for i in range(pop_size2):
        for index in range(pop_size):
            vary = 0
            mutation_prob = random.randint(0, 10)
            if mutation_prob < 3:
                if index <= 4:
                    vary = 1 + random.uniform(-0.05, 0.05)
                else:
                    vary = random.uniform(0, 1)
                rem = initial_population[index]*vary

                if abs(rem) < 10:
                    first_population[i][index] = rem
                elif abs(first_population[i][index]) >= 10:
                    first_population[i][index] = random.uniform(-1,1)

    return first_population

def crossover(parent1, parent2):
    child1 = np.zeros(11)
    child2 = np.zeros(11)

    u = random.uniform(0, 0.99)
    n_c = 5

    if (u < 0.5):
        beta = (2 * u)**((n_c + 1)**-1)
    else:
        beta = ((2*(1-u))**-1)**((n_c + 1)**-1)

    parent1 = np.array(parent1)
    parent2 = np.array(parent2)
    child1 = 0.5*((1 + beta) * parent1 + (1 - beta) * parent2)
    child2 = 0.5*((1 - beta) * parent1 + (1 + beta) * parent2)

    return np.copy(mutation(child1, 0.272727, 0.9, 1.1)), np.copy(mutation(child2, 0.272727, 0.9, 1.1))

generation = 0
fitness_pop = np.zeros(pop_size2)
prob_pop = np.zeros(pop_size2)
# parents = [0 for i in range(10)]

parents = get_initial_population()
# print(parents)

# for i in range(10):
#     parents[i] = np.copy(mutation(initial_population, 0.272727, 0.9, 1.1))

fertile_parents = np.zeros(pop_size2)

children = np.zeros(pop_size2)

colonization = []
colonization_fitness = []

crossover_probability = 0.272727

while generation < 20:
    for i in range(pop_size2):

        colonization.append(parents[i])
        errors = get_errors(SECRET_KEY, parents[i].tolist())
        
        with open("logs.txt", "a", encoding="utf8") as text_file:
            print("GENERATION: ", generation, file=text_file)
            print("PARENTS: ", parents[i], file=text_file)
            print("ERRORS: ", errors, file=text_file)

        fitness_pop[i] = fitness(errors[0], errors[1])
        colonization_fitness.append(fitness_pop[i])

    # for i in range(pop_size2):
    #     total_err = np.sum(fitness_pop)
    #     prob_pop[i] = (fitness_pop[i]/total_err)

    # idx = [i for i in range(pop_size2)]
    # fertile_parents_idx = np.random.choice(idx, pop_size2, p=prob_pop)

    np_fitness = np.copy(colonization_fitness)
    np_colonization = np.copy(colonization)

    fertile_parents_idx = np_colonization[np.argsort(np_fitness)]
    fertile_parents_idx = fertile_parents_idx[-1*pop_size2:]

    for i in range(pop_size2):
        with open("logs.txt", "a", encoding="utf8") as text_file:
            print("FERTILE PARENTS: ", fertile_parents_idx[i], file=text_file)

    mate_count = 0

    while mate_count < 10:
        offspring1, offspring2 = crossover(fertile_parents_idx[mate_count], fertile_parents_idx[mate_count+1])
        parents[mate_count] = offspring1
        parents[mate_count+1] = offspring2
        mate_count += 2

    generation += 1

    with open("logs.txt", "a", encoding="utf8") as text_file:
        print("====================================================", file=text_file)

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
