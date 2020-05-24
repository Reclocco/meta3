from __future__ import print_function

import math
import random
import sys
import copy
import numpy as np
from time import perf_counter

lab_map = []
population = 0
reproductive = 2
start = []
paths = []
stagnation = 0


def mutate():
    global paths

    for path in range(len(paths)):
        backup = copy.deepcopy(paths[path])
        for i in range(5):
            for idx in range(len(paths[path])):
                if random.randint(1, 3) == 1:
                    paths[path][idx] = random.randint(0, 3)

            if walk(paths[path]) is not None:
                paths[path] = walk(paths[path])
            else:
                paths[path] = copy.deepcopy(backup)


def switch(x, y):
    tmp = x
    x = y
    y = tmp

    return [x, y]


def indexes(word_len):
    i = random.randint(0, word_len)
    j = random.randint(0, word_len)

    return [i, j]


def walk(path):
    global lab_map
    global start

    position = copy.deepcopy(start)

    walked = []
    # eprint(path)

    for idx in range(len(path)):
        if path[idx] == 0:  # RIGHT
            if lab_map[position[0]][position[1] + 1] != 1:
                position[1] += 1
                walked.append(0)

        if path[idx] == 1:  # LEFT
            if lab_map[position[0]][position[1] - 1] != 1:
                position[1] -= 1
                walked.append(1)

        if path[idx] == 2:  # DOWN
            if lab_map[position[0] + 1][position[1]] != 1:
                position[0] += 1
                walked.append(2)

        if path[idx] == 3:  # UP
            if lab_map[position[0] - 1][position[1]] != 1:
                position[0] -= 1
                walked.append(3)

        if lab_map[position[0]][position[1]] == 8:
            return walked

    return None


def recombine(father, mother):
    global lab_map

    new_father = copy.deepcopy(father)
    new_mother = copy.deepcopy(mother)

    if len(father) < len(mother):
        length = len(father)
    else:
        length = len(mother)

    for _ in range(5):
        idxs = indexes(length - 1)
        i = idxs[0]
        j = idxs[1]

        new_father[i] = mother[i]
        new_father[j] = mother[j]

        if walk(new_father) is not None:
            break
        else:
            new_father = copy.deepcopy(father)

    for _ in range(5):
        idxs = indexes(length - 1)
        i = idxs[0]
        j = idxs[1]

        new_mother[i] = father[i]
        new_mother[j] = father[j]

        if walk(new_mother) is not None:
            break
        else:
            new_mother = copy.deepcopy(mother)

    return [new_father, new_mother]


def wheres_waldo(my_map):
    waldo = [0, 0]

    for i in range(len(my_map)):
        for j in range(len(my_map[1])):
            if my_map[i][j] == 5:
                waldo = [i, j]

    return waldo


def get_aristocrats(monsters):
    evaluated = list(map(len, monsters[::]))

    idxs = np.zeros((len(evaluated), 2))
    for i in range(len(evaluated)):
        idxs[i, 0] = i
    idxs[:, 1] = evaluated

    idxs = idxs[np.argsort(idxs[:, 1])]

    return list(map(int, idxs[:reproductive, 0]))


def main():
    global population, stagnation
    global lab_map
    global start
    global paths

    tmp = list(map(int, input().split()))
    time = tmp.pop(0)
    m = tmp.pop(0)
    n = tmp.pop(0)
    ancestors = tmp.pop(0)
    population = tmp.pop(0)

    for i in range(m):
        lab_map.append(list(map(int, [digit for digit in input()])))

    for i in range(ancestors):
        paths.append(from_char([c for c in input()]))

    best = paths[0]
    final_best = paths[0]
    aristocrats = []
    start = wheres_waldo(lab_map)

    for i in range(population - ancestors):
        paths.append(paths[i % len(paths)])

    aristocrats = get_aristocrats(paths)
    best = paths[aristocrats[0]]
    final_best = paths[aristocrats[0]]

    eprint(paths)
    eprint(time, m, n, ancestors, population)

    t_start = perf_counter()
    while time - (perf_counter() - t_start) > 0:
        for i in range(math.floor(reproductive / 2)):
            new = recombine(paths[aristocrats[2*i]], paths[aristocrats[2*i + 1]])
            paths[aristocrats[2 * i]] = new[0]
            paths[aristocrats[2 * i + 1]] = new[1]

        mutate()

        aristocrats = get_aristocrats(paths)

        best = paths[aristocrats[0]]

        if len(best) < len(final_best):
            eprint("new best!", best, len(best))
            final_best = copy.deepcopy(best)

        elif len(best) == len(final_best):
            stagnation += 1

        if stagnation == 2000:
            eprint("stagnation")
            break

    print(len(to_char(final_best)))
    eprint(to_char(final_best))


def to_char(my_path):
    chars = []
    for i in range(len(my_path)):
        if my_path[i] == 0:
            chars.append("R")
        elif my_path[i] == 1:
            chars.append("L")
        elif my_path[i] == 2:
            chars.append("D")
        elif my_path[i] == 3:
            chars.append("U")

    return chars


def from_char(my_path):
    ints = []
    for i in range(len(my_path)):
        if my_path[i] == "R":
            ints.append(0)
        elif my_path[i] == "L":
            ints.append(1)
        elif my_path[i] == "D":
            ints.append(2)
        elif my_path[i] == "U":
            ints.append(3)

    return ints


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


main()
