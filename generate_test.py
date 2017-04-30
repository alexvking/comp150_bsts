# generate_test.py
# COMP 150
# Created by Cori Jacoby
# 4/12/2017

# Tools to generate different types of test data

import random
from collections import Counter

#generate test file and prob values given number of values and range
def generate_test(element_range, num_checks):
    test_list = []

    for x in range(num_checks):
        test_list.append(random.randint(0, element_range))

    probs = [float(0)] * (element_range + 1)

    print test_list

    for x in test_list:
        probs[x] += 1 / float(num_checks)

    print probs

    alphas = []
    betas = []
    i = 0

    while i < (len(probs) - 1):
        alphas.append(probs[i])
        i += 1
        betas.append(probs[i])
        i += 1

    alphas.append(probs[i])

    assert(i == (len(probs) - 1))

    return (test_list, betas, alphas)

#generate a list of a given number of searches given alpha and beta values
def generate_search(alphas, betas, num_search, values):
    test_list = []
    insert_num = 0

    for i in range(len(betas)):
        for e in range(int(alphas[i] * num_search)):
            test_list.append(values[insert_num])
        insert_num += 1

        for e in range(int(betas[i] * num_search)):
            test_list.append(values[insert_num])
        insert_num += 1

    for e in range(int(alphas[len(betas)] * num_search)):
        test_list.append(values[insert_num])

    #could shuffle so it looks random
    return (test_list)

#generate a search list with fuzz given alphas and betas
def generate_fuzz_search(alphas, betas, num, keys):
    test_list = []

    all_probs = [0] * (len(alphas) + len(betas))

    for i in range(len(alphas)):
        all_probs[i * 2] = alphas[i]

    for i in range(len(betas)):
        all_probs[i * 2 + 1] = betas[i]

    sum_probs = [0] * len(all_probs)
    for i in range(len(all_probs)):
        sum_probs[i] = sum_probs[i-1] + all_probs[i]

    for i in range(num):
        indicator = random.random()
        for j in range(len(sum_probs)):
            if indicator < sum_probs[j]:
                test_list.append(keys[j])
                break

    return (test_list)

def generate_probs(data):
    total = len(data)

    counts = Counter(data)
    
    beta_values = []
    alphas = []
    betas = []

    num = 0

    it = iter(sorted(counts.iteritems()))

    for (k, c) in it:
        if num == 0:
            alphas.append(c/float(total))
            num = 1
        else:
            betas.append(c/float(total))
            beta_values.append(k)
            num = 0

    if len(alphas) == len(betas):
        alphas.append(0.0)

    return (alphas, betas, beta_values)