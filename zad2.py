from __future__ import print_function

import random
import sys
import copy
import numpy as np
from Rb_Tree import RbTree
from time import perf_counter


file = open("dict.txt", 'r').read().split()
dictionary = RbTree()
for line in file:
    dictionary.insert(line)


values = np.array(())
letters = []
words = []
population = 0
reproductive = 0
change = 0
stagnation = 0

final_best = []


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def mutate():
    global values
    global dictionary
    global change
    global words

    for word in range(len(words)):
        prev = copy.deepcopy(words[word])

        for i in range(10):
            for letter in range(len(words[word])):
                if random.randint(1, 5) == 1:
                    words[word][letter] = random.choice(letters)
            if random.randint(1, 4) == 1:
                words[word] += random.choice(letters)

            if dictionary.find(''.join(words[word])) == 1:
                change = 1
                break
            else:
                words[word] = copy.deepcopy(prev)


def evaluate(word):
    global values
    global letters

    value = 0
    for i in range(len(word)):

        try:
            value += values[1, letters.index(word[i])]
        except ValueError:
            pass

    return value


def switch(x, y):
    tmp = x
    x = y
    y = tmp

    return [x, y]


def indexes(word_len):
    i = random.randint(0, word_len)
    j = random.randint(0, word_len)

    return [i, j]


def recombine(father, mother):
    global change
    global dictionary

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

        if dictionary.find(''.join(new_father)) == 1:
            change = 1
            break
        else:
            new_father = copy.deepcopy(father)

    for _ in range(5):
        idxs = indexes(length - 1)
        i = idxs[0]
        j = idxs[1]

        new_mother[i] = father[i]
        new_mother[j] = father[j]

        if dictionary.find(''.join(new_mother)) == 1:
            change = 1
            break
        else:
            new_mother = copy.deepcopy(mother)

    return [new_father, new_mother]


def get_aristocrats(monsters):
    evaluated = list(map(evaluate, monsters[::]))

    idxs = np.zeros((len(evaluated), 2))
    for i in range(len(evaluated)):
        idxs[i, 0] = i
    idxs[:, 1] = evaluated

    idxs = idxs[np.argsort(idxs[:, 1])]

    return list(map(int, idxs[reproductive:, 0]))


def main():
    global values
    global letters
    global final_best
    global population
    global reproductive
    global change
    global stagnation
    population = 10
    reproductive = 2

    my_input = list(map(int, input().split()))
    time = my_input.pop(0)
    l_count = my_input.pop(0)
    w_count = my_input.pop(0)

    values = np.array([[1 for _ in range(l_count)], [1 for _ in range(l_count)]])

    for i in range(l_count):
        my_input = input().split()
        values[0, i] = i
        letters.append(my_input[0])
        values[1, i] = my_input[1]

    for i in range(w_count):
        words.append(list(input()))

    for i in range(population - w_count):
        words.append(copy.deepcopy(words[i % l_count]))

    aristocracy = get_aristocrats(words)
    best = words[aristocracy[-1]]
    final_best = words[aristocracy[-1]]

    t_start = perf_counter()
    while time - (perf_counter() - t_start) > 0:
        for i in range(int(reproductive / 2)):
            new = recombine(words[aristocracy[i]], words[aristocracy[i + 1]])
            words[aristocracy[i]] = copy.deepcopy(new[0])
            words[aristocracy[i + 1]] = copy.deepcopy(new[1])

        mutate()

        aristocracy = get_aristocrats(words)

        best = words[aristocracy[-1]]
        if evaluate(best) > evaluate(final_best):
            eprint("new best!", best, evaluate(best))
            final_best = copy.deepcopy(best)

        if stagnation == 2:
            eprint("stagnation")
            break

        if change == 0:
            stagnation += 1
        else:
            stagnation = 0

    eprint(words, "\n")
    eprint("BEST: ", ''.join(final_best))
    print(evaluate(final_best))


main()
