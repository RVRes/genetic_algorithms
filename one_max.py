import random

import matplotlib.pyplot as plt

# константы задачи
ONE_MAX_LENGTH = 100  # длина битовой строки, подлежащей оптимизации

# константы генетического алгоритма
POPULATION_SIZE = 200  # количество индивидумов в популяции
P_CROSSOVER = 0.9  # вероятность скрещевания
P_MUTATION = 0.1  # вероятность мутации
MAX_GENERATIONS = 100  # максимальное количество поколений

# RANDOM_SEED = 42
# random.seed(RANDOM_SEED)


class FitnessMax:
    def __init__(self):
        self.values = [0]


class Individual(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = FitnessMax()

    def __str__(self):
        return str(self)


def one_max_fitness(individual):
    return sum(individual)  # кортеж


def individual_creator():
    return Individual([random.randint(0, 1) for _ in range(ONE_MAX_LENGTH)])


def population_creator(n=0):
    return list([individual_creator() for _ in range(n)])


population = population_creator(n=POPULATION_SIZE)
generation_counter = 0

fitness_values = list(map(one_max_fitness, population))
for individual, fitness_value in zip(population, fitness_values):
    individual.fitness.values = fitness_value

max_fitness_values = []
mean_fitness_values = []


def clone(value):
    ind = Individual(value[:])
    ind.fitness.values = value.fitness.values
    return ind


def sel_tournament(population, p_len):
    offspring = []
    for n in range(p_len):
        i1 = i2 = i3 = 0
        while i1 == i2 or i1 == i3 or i2 == i3:  # TODO а не or ли здесь? было and
            i1, i2, i3 = (random.randint(0, p_len - 1) for _ in range(3))
        offspring.append(max([population[i1], population[i2], population[i3]], key=lambda ind: ind.fitness.values))
    return offspring


def cx_one_point(child1, child2):
    s = random.randint(2, len(child1) - 3)
    child1[:s], child2[s:] = child2[:s], child1[s:]


def mut_flit_bit(mutant, indpb=0.01):
    for indx in range(len(mutant)):
        if random.random() < indpb:
            mutant[indx] = 0 if mutant[indx] == 1 else 1


fitness_values = [individual.fitness.values for individual in population]

while max(fitness_values) < ONE_MAX_LENGTH and generation_counter < MAX_GENERATIONS:
    generation_counter += 1
    offspring = sel_tournament(population, len(population))
    offspring = list(map(clone, offspring))

    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < P_CROSSOVER:
            cx_one_point(child1, child2)

    for mutant in offspring:
        if random.random() < P_MUTATION:
            mut_flit_bit(mutant, indpb=1.0 / ONE_MAX_LENGTH)

    fresh_fitness_values = list(map(one_max_fitness, offspring))
    for individual, fitness_value in zip(offspring, fresh_fitness_values):
        individual.fitness.values = fitness_value

    population[:] = offspring

    fitness_values = [ind.fitness.values for ind in population]
    max_fitness = max(fitness_values)
    mean_fitness = sum(fitness_values) / len(population)
    max_fitness_values.append(max_fitness)
    mean_fitness_values.append(mean_fitness)
    print(f'Поколение {generation_counter}: Макс. приспособ. = {max_fitness}, Средн. приспособ. = {mean_fitness}')
    best_index = fitness_values.index(max(fitness_values))
    print('Лучший индивидуум = ', *population[best_index], '\n')

plt.plot(max_fitness_values, color='red')
plt.plot(mean_fitness_values, color='green')
plt.xlabel('Поколение')
plt.ylabel('Макс/средняя приспособленность')
plt.title('Зависимость максимальной и средней приспособленности от поколения')
plt.show()