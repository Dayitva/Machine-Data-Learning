import random
from client import *

# overfit_file = open("overfit.txt", "r")
# initial_population = overfit_file.read()

initial_population = [0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11,
                      -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,
                      2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]

# train_error, validation_error = [13510723304.19212, 368296592820.6967]

def fitness():
    pass

def mutation(population):
    mutation_factor = random.uniform(-1, 1)
    return [random.choice([i, i*mutation_factor]) for i in population]

def crossover():
    pass

for i in initial_population:
    error = get_errors(SECRET_KEY, mutation(initial_population))
    print(error)
    # print(mutation(initial_population))
    