# benchmarking.py
# COMP 150
# Created by Cori Jacoby and Alex King
# 4/11/2017

# Testing runtimes of different binary search tree construction algorithms

# File opening, timing, and test data creation
import sys
import time
from random import shuffle
from generate_test import generate_probs, generate_fuzz_search, generate_search

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

    # TODO: parameterize the following bits of information as command line
    # arguments:
    #  - test file (give file name)
    #  - number of words to read (minimum 1; if > total words, just use all)
    #  - number of searches to do (num_searches)

    # TODO: new functionality:
    #  - Do math at the end to compare runtimes of nlogn and n^2, such that
    #    we're able to report approximately how many searches would be required
    #    to make the n^2 tree "worth it"

    # Convert text document of English words into Python list of strings/words
    corpus = [word for line in 
              open("test_data/warandpeace.txt", 'r') for word in line.split()]

    # Take a subset of the entire corpus
    corpus = corpus[:50000]

    (alphas, betas, beta_values) = generate_probs(corpus)

    print "CORPUS = WAR AND PEACE\n"
    print "total words:", len(corpus), "keys:", len(beta_values)

    # generate fuzz search
    num_searches = 10000
    print "Generating test lists..."
    fuzz_search_list = generate_fuzz_search(alphas, betas, num_searches, corpus)
    search_list = generate_search(alphas, betas, num_searches, corpus)
    shuffle(search_list)

    # define number of corpus repeats
    corpus_repeats = 2

    ### Tree Testing

    print "NLOGN:"
    # nlogn
    start = time.time()
    tree = Nlogn_build(betas, alphas, len(betas), beta_values, min(betas) / 2)
    end = time.time()
    print "Construct time:", end-start

    start = time.time()
    depths = []
    for x in range(corpus_repeats):
        for k in corpus:
            depths.append(tree.find(k, 0)[1])
    end = time.time()
    print corpus_repeats,"x Corpus search time and avg:", end-start, (end-start)/len(corpus)
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in search_list:
        depths.append(tree.find(k, 0)[1])
    end = time.time()
    print num_searches, "Proportional search time and average:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in fuzz_search_list:
        depths.append(tree.find(k, 0)[1])
    end = time.time()
    print num_searches, "Fuzz search time and average", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)



    print
    print "NAIVE BST"
    values = [i for i in range(len(betas))]
    shuffle(values)
    # print bs[0], aes[0], len(bs), len(aes)
    start = time.time()
    t = BSTTree(None)
    for v in values:
        t.insert(beta_values[v])
    end = time.time()

    print "Build time:", end-start

    depths = []
    start = time.time()
    for x in range(corpus_repeats):
        for k in corpus:
            depths.append(t.find(k, 0)[1])
    end = time.time()
    print corpus_repeats, "x Corpus search time and avg:", end-start, (end-start)/len(corpus)
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in search_list:
        depths.append(t.find(k, 0)[1])
    end = time.time()
    # print t
    print num_searches, "proportional search and avg:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in fuzz_search_list:
        depths.append(t.find(k, 0)[1])
    end = time.time()
    print num_searches, "fuzz search and avg:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)



    print
    print "AVL BST"
    start = time.time()
    t = AVLTree(values[0])
    for v in values[1:]:
        t = t.insert(beta_values[v])
    end = time.time()

    print "Build time:", end-start

    depths = []
    start = time.time()
    for x in range(corpus_repeats):
        for k in corpus:
            depths.append(t.find(k, 0)[1])
    end = time.time()
    print corpus_repeats, "x Corpus search time and avg:", end-start, (end-start)/len(corpus)
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in search_list:
        depths.append(t.find(k, 0)[1])
    end = time.time()
    # print t
    print num_searches, "proportional search and avg:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in fuzz_search_list:
        depths.append(t.find(k, 0)[1])
    end = time.time()
    print num_searches, "fuzz search and avg:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)



    print
    print "KNUTH RULE 1 HEURISTIC BST"
    start = time.time()
    t = Knuth_Rule1(betas, alphas, len(betas), beta_values)
    end = time.time()

    print "Build time:", end-start

    depths = []
    start = time.time()
    for x in range(corpus_repeats):
        for k in corpus:
            depths.append(t.find(k, 0)[1])
    end = time.time()
    print corpus_repeats, "x Corpus search time and avg:", end-start, (end-start)/len(corpus)
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in search_list:
        depths.append(t.find(k, 0)[1])
    end = time.time()
    # print t
    print num_searches, "proportional search and avg:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in fuzz_search_list:
        depths.append(t.find(k, 0)[1])
    end = time.time()
    print num_searches, "fuzz search and avg:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)



    print
    print "KNUTH N^2"
    # n^2
    start = time.time()
    (exp, root) = Knuth_find(betas, alphas, len(betas))
    tree = Knuth_build(root, beta_values)
    end = time.time()
    print "Construction time:", end-start

    depths = []
    start = time.time()
    for x in range(corpus_repeats):
        for k in corpus:
            depths.append(tree.find(k, 0)[1])
    end = time.time()
    print corpus_repeats,"x Corpus search time and avg:", end-start, (end-start)/len(corpus)
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in search_list:
        #tree.find(beta_values[k/2])
        depths.append(tree.find(k, 0)[1])
    end = time.time()
    print num_searches, "Proportional search and avg:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in fuzz_search_list:
        depths.append(tree.find(k, 0)[1])
    end = time.time()
    print num_searches, "fuzz search time and avg:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)


test()