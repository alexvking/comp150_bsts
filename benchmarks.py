# benchmarks.py
# COMP 150
# Created by Cori Jacoby and Alex King
# 5/4/2017

# Testing runtimes of different binary search tree construction algorithms

# File opening, timing, and test data creation
import sys
import time
import resource
from random import shuffle
from generate_test import generate_probs, generate_fuzz_search, generate_search,\
                          generate_probs_high_leaf, generate_probs_high_key,\
                          generate_probs_uniform

# Basic trees
from BSTTree import BSTTree
from AVLTree import AVLTree

# Knuth's n^2 tree
from optimal_bst_knuth import find_optimal_tree_ordering as Knuth_find
from optimal_bst_knuth import construct_tree_inline as Knuth_build

# Mehlhorn's n*logn approximation
from approximate_bst_mehlhorn import find_optimal_tree_ordering as Nlogn_build

# Knuth's "bad rule" approximation
from highest_prob_root import find_optimal_tree_ordering as Knuth_Rule1

def test():
    """
    Test function to build trees based on corpus specified
    """

    if len(sys.argv) < 2:
        print "Usage: python benchmarks.py corpus.txt num_words test_type"
        exit(1)

    corpusfile = sys.argv[1]
    num_words = 10000
    small_words = 10000
    big_words = 160000
    num_searches = 100000
    test_type = "small"
    if len(sys.argv) != 4:
        print "Usage: python benchmarks.py corpus.txt num_words test_type"
        exit(1)
    else:
        num_words = int(sys.argv[2])
        test_type = sys.argv[3]

    even_dist_keys = 3000

    random_repeats = 3

    # Convert text document of English words into Python list of strings/words
    corpus = [word for line in 
              open(corpusfile, 'r') for word in line.split()]

    standard_corp = corpus[:num_words]

    # define number of corpus repeats
    corpus_repeats = 2

    #to fill in
    datasets = []

    if test_type == "small":
        #small dataset
        datasets.append(("small dataset", generate_probs(corpus[:small_words]), corpus[:small_words]))
    elif test_type == "medium":
        #medium dataset
        datasets.append(("medium dataset", generate_probs(standard_corp), standard_corp))
    elif test_type == "large":
        #large dataset
        datasets.append(("large dataset", generate_probs(corpus[:big_words]), corpus[:big_words]))
    elif test_type == "leaf":
        #high leaf probabilties
        datasets.append(("high leaf dataset", generate_probs_high_leaf(standard_corp), standard_corp))
    elif test_type == "key":   
        #high key probabilties
        datasets.append(("high key ds", generate_probs_high_key(standard_corp[:num_words/2]), standard_corp[:num_words/2]))
    elif test_type == "uniform": 
        #uniform dataset
        datasets.append(("uniform ds", generate_probs_uniform(even_dist_keys), [i for i in range(even_dist_keys)]))

    for (name, (alphas, betas, beta_values), corpora) in datasets:
        print "========================================"
        print "running", name
        print len(beta_values)
        insert_indices = [i for i in range(len(beta_values))]
        shuffle(insert_indices)

        searches = corpora

        #MEHLHORN 
        print
        print "MEHLHORN KNUTH"
        start = time.time()
        nlogntree = Nlogn_build(betas, alphas, len(betas), beta_values, min(betas) / 2)
        end = time.time()
        cons_time = end-start

        depths = []
        start = time.time()
        for x in range(corpus_repeats):
            for k in searches:
                depths.append(nlogntree.find(k)[1])
        end = time.time()
        print "BUILD TIME:", cons_time, "AVG SEARCH TIME:", (end-start)/(len(searches) * corpus_repeats), "AVG DEPTH:", float(sum(depths))/len(depths)

        #KNUTH OPTION 1
        print
        print "KNUTH ROOT METHOD"
        start = time.time()
        root_tree = Knuth_Rule1(betas, alphas, len(betas), beta_values)
        end = time.time()
        cons_time = end-start

        depths = []
        start = time.time()
        for x in range(corpus_repeats):
            for k in searches:
                depths.append(root_tree.find(k)[1])
        end = time.time()
        print "BUILD TIME:", cons_time, "AVG SEARCH TIME:", (end-start)/(len(searches) * corpus_repeats), "AVG DEPTH:", float(sum(depths))/len(depths)


        #AVL
        print
        print "AVL"
        avg_build_time = 0.0
        avg_depth = 0.0
        for x in range(random_repeats):
            start = time.time()
            avl_tree = AVLTree(None)
            for v in insert_indices:
                avl_tree = avl_tree.insert(beta_values[v])
            end = time.time()
            cons_time = end-start

            depths = []
            start = time.time()
            for x in range(corpus_repeats):
                for k in searches:
                    depths.append(avl_tree.find(k)[1])
            end = time.time()
            avg_build_time += cons_time
            avg_depth += float(sum(depths))/len(depths)
        print "BUILD TIME:", avg_build_time/random_repeats, "AVG SEARCH TIME:", (end-start)/(len(searches) * corpus_repeats), "AVG DEPTH:", avg_depth/random_repeats

        #NAIVE BST
        print
        print "NAIVE BST"
        avg_build_time = 0.0
        avg_depth = 0.0
        for x in range(random_repeats):
            start = time.time()
            bst_tree = BSTTree(None)
            for v in insert_indices:
                bst_tree.insert(beta_values[v])
            end = time.time()
            cons_time = end-start

            depths = []
            start = time.time()
            for x in range(corpus_repeats):
                for k in searches:
                    depths.append(bst_tree.find(k)[1])
            end = time.time()
            avg_build_time += cons_time
            avg_depth += float(sum(depths))/len(depths)
        print "BUILD TIME:", avg_build_time/random_repeats, "AVG SEARCH TIME:", (end-start)/(len(searches) * corpus_repeats), "AVG DEPTH:", avg_depth/random_repeats


        #KNUTH
        print
        print "OPTIMAL KNUTH"
        start = time.time()
        (exp, root) = Knuth_find(betas, alphas, len(betas))
        Knuth_tree = Knuth_build(root, beta_values)
        end = time.time()
        cons_time = end-start

        depths = []
        start = time.time()
        for x in range(corpus_repeats):
            for k in searches:
                depths.append(Knuth_tree.find(k)[1])
        end = time.time()
        print "BUILD TIME:", cons_time, "AVG SEARCH TIME:", (end-start)/(len(searches) * corpus_repeats), "AVG DEPTH:", float(sum(depths))/len(depths)

        print "\nMemory:", float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000000, "megaytes used"


test()
