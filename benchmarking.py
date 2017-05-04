# benchmarking.py
# COMP 150
# Created by Cori Jacoby and Alex King
# 4/11/2017

# Testing runtimes of different binary search tree construction algorithms

# File opening, timing, and test data creation
import sys
import time
import resource
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

    if len(sys.argv) < 2:
        print "Usage: python benchmarking.py corpus.txt num_words num_searches"
        exit(1)

    corpusfile = sys.argv[1]
    num_words = 10000
    num_searches = 100000
    if len(sys.argv) >= 3:
        num_words = int(sys.argv[2])
    if len(sys.argv) == 4:
        num_searches = int(sys.argv[3])

    # Convert text document of English words into Python list of strings/words
    corpus = [word for line in 
              open(corpusfile, 'r') for word in line.split()]

    # Take a subset of the entire corpus
    corpus = corpus[:num_words]

    (alphas, betas, beta_values) = generate_probs(corpus)

    print "CORPUS =", corpusfile
    print "total words:", len(corpus), "keys:", len(beta_values)

    # generate fuzz search
    print "Generating test lists...\n"
    fuzz_search_list = generate_fuzz_search(alphas, betas, num_searches, corpus)
    search_list = generate_search(alphas, betas, num_searches, corpus)
    shuffle(search_list)

    # define number of corpus repeats
    corpus_repeats = 2

    ### Tree Testing

    print "NLOGN"
    # nlogn
    start = time.time()
    tree = Nlogn_build(betas, alphas, len(betas), beta_values, min(betas) / 2)
    end = time.time()
    print "Construct time:", end-start
    nlogn_build_time = end-start

    start = time.time()
    depths = []
    for x in range(corpus_repeats):
        for k in corpus:
            depths.append(tree.find(k)[1])
    end = time.time()
    print corpus_repeats,"x Corpus search time and avg:", end-start, (end-start)/len(corpus)
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in search_list:
        depths.append(tree.find(k)[1])
    end = time.time()
    print num_searches, "Proportional search time and average:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)
    nlogn_avg_search = (end-start)/num_searches

    depths = []
    start = time.time()
    for k in fuzz_search_list:
        depths.append(tree.find(k)[1])
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
            depths.append(t.find(k)[1])
    end = time.time()
    print corpus_repeats, "x Corpus search time and avg:", end-start, (end-start)/len(corpus)
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in search_list:
        depths.append(t.find(k)[1])
    end = time.time()
    # print t
    print num_searches, "proportional search and avg:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in fuzz_search_list:
        depths.append(t.find(k)[1])
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
            depths.append(t.find(k)[1])
    end = time.time()
    print corpus_repeats, "x Corpus search time and avg:", end-start, (end-start)/len(corpus)
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in search_list:
        depths.append(t.find(k)[1])
    end = time.time()
    # print t
    print num_searches, "proportional search and avg:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in fuzz_search_list:
        depths.append(t.find(k)[1])
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
            depths.append(t.find(k)[1])
    end = time.time()
    print corpus_repeats, "x Corpus search time and avg:", end-start, (end-start)/len(corpus)
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in search_list:
        depths.append(t.find(k)[1])
    end = time.time()
    # print t
    print num_searches, "proportional search and avg:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in fuzz_search_list:
        depths.append(t.find(k)[1])
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
    n2_build_time = end-start

    depths = []
    start = time.time()
    for x in range(corpus_repeats):
        for k in corpus:
            depths.append(tree.find(k)[1])
    end = time.time()
    print corpus_repeats,"x Corpus search time and avg:", end-start, (end-start)/len(corpus)
    print float(sum(depths)) / len(depths)

    depths = []
    start = time.time()
    for k in search_list:
        depths.append(tree.find(k)[1])
    end = time.time()
    print num_searches, "Proportional search and avg:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)
    n2_avg_search = (end-start)/num_searches

    depths = []
    start = time.time()
    for k in fuzz_search_list:
        depths.append(tree.find(k)[1])
    end = time.time()
    print num_searches, "fuzz search time and avg:", end-start, (end-start)/num_searches
    print float(sum(depths)) / len(depths)


    # Finally, calculate the intercept of our two most compelling algorithms
    # to demonstrate the practical tradeoff
    print "\nIn order for the Knuth algorithm to be worth your time, you will\n", \
          "need to anticipate making at least %d searches." % \
          int((-(nlogn_build_time - n2_build_time))/
           (nlogn_avg_search - n2_avg_search))

    print "\nMemory:", float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1000000, "megaytes used"


test()