import random
from pprint import pprint
import matplotlib.pyplot as plt

# RANDOM_SEED = 42
# random.seed(RANDOM_SEED)

ITEMS_COUNT = 20  # вещей в куче до загрузки в рюкзак
ITEMS = {
    'weight': [random.randint(1, 5) for _ in range(ITEMS_COUNT)],
    'price': [random.randint(1, 100) for _ in range(ITEMS_COUNT)]
}
BAG_SIZE = 1000 # максимальный вес рюкзака

# ITEMS_COUNT = 3
# ITEMS = {
#     'weight': [1, 4, 3],
#     'price': [1500, 3000, 2000]
# }
# BAG_SIZE = 4  # максимальный вес рюкзака

# ITEMS_COUNT = 4
# ITEMS = {
#     'weight': [5, 4, 10, 9],
#     'price': [7, 6, 3, 5]
# }
# BAG_SIZE = 19  # максимальный вес рюкзака

# настройки генетического алгоритма
POPULATION_SIZE = 30
P_CROSSOVER = 0.9
P_MUTATION = 0.1
MAX_GENERATIONS = 15


def get_weight(ind: list):
    return sum(map(lambda x, y: x * y, ITEMS['weight'], ind))


def get_price(ind: list):
    return sum(map(lambda x, y: x * y, ITEMS['price'], ind))


def individual_is_valid(ind: list):
    return True if get_weight(ind) <= BAG_SIZE else False


def generate_valid_individual():
    individual = None
    while not individual or not individual_is_valid(individual):
        individual = [random.randint(0, 1) if ITEMS['weight'][i] <= BAG_SIZE else 0 for i in range(ITEMS_COUNT)]
    print(individual)
    return individual


def sel_tournament(population):
    len_p = len(population)
    offspring = []
    for n in range(len_p):
        i1 = i2 = i3 = 0
        while i1 == i2 or i1 == i3 or i2 == i3:
            i1, i2, i3 = (random.randint(0, len_p - 1) for _ in range(3))
        tournament_list = (population[i1], population[i2], population[i3])
        price_list = list((map(get_price, tournament_list)))
        offspring.append(list(max(zip(price_list, tournament_list))[1]))
    return offspring


def cx_one_point(child1: list, child2: list):
    s = random.randint(1, len(child1) - 2)
    result1, result2 = [], []
    result1[:], result2[:] = child1, child2
    result1[:s], result2[s:] = child2[:s], child1[s:]
    if individual_is_valid(result1):
        child1 = result1
    if individual_is_valid(result2):
        child2 = result2


def mut_flit_bit(mutant, indpb=0.01):
    for indx in range(len(mutant)):
        if random.random() < indpb:
            mutant_candidate = list(mutant)
            mutant_candidate[indx] = 0 if mutant[indx] == 1 else 1
            if individual_is_valid(mutant_candidate):
                mutant = mutant_candidate


population = [generate_valid_individual() for __ in range(POPULATION_SIZE)]
generation_count = 0
max_prices = []
mean_prices = []
ind_weight = []

# print(*[f'{sum(map(lambda x, y: x * y, ITEMS["weight"], ind))}, {ind}' for ind in population])

while generation_count <= MAX_GENERATIONS:
    generation_count += 1

    offspring = sel_tournament(population)
    # print('Tourn: ',*[f'{sum(map(lambda x, y: x * y, ITEMS["weight"], ind))}, {ind}' for ind in offspring])

    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < P_CROSSOVER:
            cx_one_point(child1, child2)

    # print('Cross: ',*[f'{sum(map(lambda x, y: x * y, ITEMS["weight"], ind))}, {ind}' for ind in offspring])

    for mutant in offspring:
        if random.random() < P_MUTATION:
            mut_flit_bit(mutant, indpb=1.0 / ITEMS_COUNT)

    # print('Mutant: ',*[f'{sum(map(lambda x, y: x * y, ITEMS["weight"], ind))}, {ind}' for ind in offspring])

    population[:] = offspring

    # print(*[f'{sum(map(lambda x, y: x * y, ITEMS["weight"], ind))}, {ind}' for ind in population])

    price_list = list(map(get_price, population))
    max_price = max(price_list)
    mean_price = sum(price_list) / len(population)
    best_individual = population[price_list.index(max_price)]
    best_individual_weight = get_weight(best_individual)
    for i in range(len(best_individual)):
        if best_individual[i] == 1:
            print(f'item {i}, weight: {ITEMS["weight"][i]}, price: {ITEMS["price"][i]}')
    print('Общий вес:', best_individual_weight)
    print('Общая цена:', max_price)
    max_prices.append(max_price)
    mean_prices.append(mean_price)
    ind_weight.append(best_individual_weight)

print('==============куча================')
for i in range(ITEMS_COUNT):
    print(f'item {i}, weight: {ITEMS["weight"][i]}, price: {ITEMS["price"][i]}')

plt.plot(max_prices, color='red')
plt.plot(mean_prices, color='green')
plt.plot(ind_weight, color='blue')
plt.xlabel('Поколение')
plt.ylabel('Макс/средняя цена/вес')
plt.title('Зависимость максимальной и средней цены от поколения')
plt.show()

# ind = [random.randint(0, 1) for _ in range(ITEMS_COUNT)]
# print(ITEMS['weight'], ind, sep='\n')
# print(*map(lambda x, y: x * y, ITEMS['weight'], ind))
# print(sum(map(lambda x, y: x * y, ITEMS['weight'], ind)))

# pprint(population)
