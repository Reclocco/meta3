import math
import random
import copy
import numpy as np
from time import perf_counter

e = []
final_best = []


def mutate(monsters):
    for x in monsters:
        for chromosome in range(len(x)):
            for element in range(len(x[chromosome])):
                if random.randint(1, 15) == 1:
                    if x[chromosome][element] == '1':
                        x[chromosome][element] = '0'
                    else:
                        x[chromosome][element] = '1'


def yang(x):
    global e

    value = 0
    for i in range(5):
        dec = int(''.join(x[i]), 2)/100 - 5

        value += e[i] * abs(dec) ** (i + 1)
    return value


def represent(x, length):
    binary = list(bin((x + 5) * 100))
    binary.pop(0)
    binary.pop(0)

    missing = length - len(binary)
    zeros = ["0" for _ in range(missing)]
    binary = zeros + list(binary)
    return binary


def switch(x, y):
    tmp = x
    x = y
    y = tmp

    return [x, y]


def indexes():
    i = random.randint(0, 10)
    j = random.randint(0, 10)
    if i > j:
        s = switch(i, j)
        i = s[0]
        j = s[1]

    return [i, j]


def recombine(father, mother):
    new_father = copy.deepcopy(father)
    new_mother = copy.deepcopy(mother)

    for chromosome in range(len(father)):
        idxs = indexes()
        i = idxs[0]
        j = idxs[1]

        for idx in range(j - i):
            new_father[chromosome][i + idx] = mother[chromosome][i + idx]

        idxs = indexes()
        i = idxs[0]
        j = idxs[1]

        for idx in range(j - i):
            new_mother[chromosome][i + idx] = father[chromosome][i + idx]

    return [new_father, new_mother]


def get_aristocrats(monsters):
    values = list(map(yang, monsters[::]))

    idxs = np.zeros((len(values), 2))
    for i in range(len(values)):
        idxs[i, 0] = i
    idxs[:, 1] = values

    idxs = idxs[np.argsort(idxs[:, 1])]

    return idxs[:6, 0]


def get_king(monsters, aristocrats):
    return monsters[int(aristocrats[0])]


def main():
    global e
    global final_best

    res = 0.02
    population = 13
    percent = 6

    my_input = list(map(int, input().split()))
    time = my_input.pop(0)
    variables = copy.deepcopy(my_input[0:5])
    e = copy.deepcopy(my_input[5:])

    for element in variables:
        if abs(element) > 5:
            print("Wrong input: |x[i]| > 5")
            return

    length = int(math.ceil(math.log(10 / res, 2)))
    x = []
    for i in range(len(variables)):
        x.append(represent(variables[i], length))

    monsters = [x for _ in range(population)]
    best = monsters[0]
    final_best = monsters[0]

    aristocracy = [i for i in range(percent)]

    t_start = perf_counter()
    while time - (perf_counter() - t_start) > 0:
        for i in range(int(percent / 2)):
            new = recombine(monsters[aristocracy[i]], monsters[aristocracy[i + 1]])
            monsters[aristocracy[i]] = copy.deepcopy(new[0])
            monsters[aristocracy[i + 1]] = copy.deepcopy(new[1])

        mutate(monsters)

        aristocrats = get_aristocrats(monsters)

        best = get_king(monsters, aristocrats)
        if yang(best) < yang(final_best):
            final_best = copy.deepcopy(best)

        if yang(best) < 1:
            print("breaking")
            break

    print("BEST: ", [(int(''.join(final_best[i]), 2)/100 - 5) for i in range(5)], yang(final_best))


main()
