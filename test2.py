NUMBERS_LIST = [1, 6, 99, 32, 54, 82, 31, 50, 48]
TARGET = 33

def nearest_index(n_list: list, target: int):
    delta = 10 ** 100
    ind_closet = None
    for ind, val in enumerate(n_list):
        temp_result = abs(val - target)
        if temp_result == 0:
            return ind
        elif temp_result < delta:
            delta = temp_result
            ind_closet = ind
    return ind_closet

print(nearest_index(NUMBERS_LIST,TARGET))