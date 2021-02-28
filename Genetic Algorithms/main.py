import random
from client import *

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

def mutation(population):
    mutation_factor = random.uniform(-1, 1)
    return [random.choice([i, i*mutation_factor]) for i in population]

def crossover(parent1, parent2):
    length1 = int(np.size(parent1)/2)
    length2 = int(np.size(parent2)/2)

    crossedParent1 = np.concatenate(parent1[:length1], parent2[length2:])
    crossedParent2 = np.concatenate(parent1[length1:], parent2[:length2])

    return crossedParent1, crossedParent2

generation = 0
fitness_pop = np.zeros(pop_size2)
prob_pop = np.zeros(pop_size2)
parents = [0 for i in range(10)]

for i in range(10):
    parents[i] = np.copy(mutation(initial_population))
    
fertile_parents = np.zeros(pop_size2)

children = np.zeros(pop_size2)

colonization = []
colonization_fitness = []

while generation < pop_size2:
    for i in range(pop_size2):
        
        colonization.append(parents[i])

        errors = get_errors(SECRET_KEY, parents[i].tolist())
        print("GENERATION: ", generation)
        print("PARENTS: ", parents[i])
        print("ERRORS: ", errors)

        fitness_pop[i] = fitness(errors[0], errors[1])
            
    for i in range(pop_size2):
        total_err = np.sum(fitness_pop)
        prob_pop[i] = (fitness_pop[i]/total_err)

    colonization_fitness.append(fitness_pop)

    idx = [i for i in range(pop_size2)]
    fertile_parents_idx = np.random.choice(idx, pop_size2, p=prob_pop)

    for i in range(pop_size2):
        print("FERTILE PARENTS: ", parents[fertile_parents_idx[i]])

    mate_count = 0

    while mate_count < 10:
        offspring1, offspring2 = crossover(parents[fertile_parents_idx[mate_count]], parents[fertile_parents_idx[mate_count+1]])
        parents[mate_count] = offspring1
        parents[mate_count+1] = offspring2
        mate_count += 2

    offspring1, offspring2 = crossover(parents[fertile_parents_idx[0]], parents[fertile_parents_idx[10]])
    parents[10] = offspring1

    generation += 1

    print("====================================================")










#Continue mutating and crossing over the individual for some iterations
#Change the fitness, mutation and crossover functions according to the errors received
