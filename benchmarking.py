# benchmarking.py
# COMP 150
# Created by Cori Jacoby and Alex King
# 4/11/2017

# Testing runtimes of different binary search tree construction algorithms

import time

# We'll clean these up once things get renamed...
from approximate_bst_knuth import find_optimal_tree_ordering as Knuth_find
from approximate_bst_knuth import construct_tree_inline as Knuth_build
from approximate_with_building import find_optimal_tree_ordering as Nlogn_build

def test():
    values = [i for i in range(1000)]
    start = time.time()
    (exp, root) = Knuth_find([0.0004997501249] * 1000, [0.0004997501249] * 1001, 1000)
    tree = Knuth_build(root, values)
    end = time.time()
    print "Time to build a Knuth tree of 1000 items:", end-start
    start = time.time()
    for x in range(200):
        for y in range(1000):
            tree.find(y)
    end = time.time()
    print "Time to search for all 1000 items 200 times each:", end-start
    print "average time per lookup:", (end-start) / (200 * 1000)

    values = [i for i in range(1000)]
    start = time.time()
    tree = Nlogn_build([0.0004997501249] * 1000, [0.0004997501249] * 1001, 1000)
    # tree = Nlogn_build([0.00004999750012] * 10000, [0.00004999750012] * 10001, 10000)
    end = time.time()
    print "Time to build O(nlogn) tree of 1000 items:", end-start
    start = time.time()
    for x in range(200):
        for y in range(1000):
            tree.find(y)
    end = time.time()
    print "Time to search for all 1000 items 200 times each:", end-start
    print "average time per lookup:", (end-start) / (200 * 1000)
    return

test()