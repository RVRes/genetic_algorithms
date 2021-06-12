from dataclasses import dataclass
import random
import string
import matplotlib.pyplot as plt
from pprint import pprint

TABLE = {
    'first_column': [i for i in range(101)],
    'second_colmn': [''.join(random.choice(string.ascii_lowercase) for _ in range(10)) for _ in range(101)],
    'third_column': [i * i for i in range(101)]
}


def list_summarize(any_list: list):
    return sum(any_list)


def render_table(table: dict):
    for i in range(max(len(data) for key, data in table.items())):
        if table[list(table.keys())[2]][i] < 100:
            print([table[key][i] for key in table.keys()])


def render_table2(t: dict):
    for key, value in t.items():
        print("{0}: {1}".format(key, value))


# print(list_summarize(TABLE['third_column']))
# pprint(TABLE)
# render_table(TABLE)

# ft = dict(filter(lambda k, val: val[2] < 100, TABLE.items()))
render_table2(TABLE)
plt.plot(TABLE[list(TABLE.keys())[0]], color='green')
# plt.plot(TABLE[list(TABLE.keys())[2]], color='red')
plt.show()

with ''
