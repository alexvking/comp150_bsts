# benchmarking.py
# COMP 150
# Created by Cori Jacoby and Alex King
# 4/11/2017

# Testing runtimes of different binary search tree construction algorithms

import time
import sys

# We'll clean these up once things get renamed...
from approximate_bst_knuth import find_optimal_tree_ordering as Knuth_find
from approximate_bst_knuth import construct_tree_inline as Knuth_build
from approximate_with_building import find_optimal_tree_ordering as Nlogn_build
from avl import AVLTree

from optimal_bst_knuth_n3 import find_optimal_tree_ordering as Knuth_n3_find
from optimal_bst_knuth_n3 import construct_tree_inline as Knuth_n3_build

from highest_prob_root import find_optimal_tree_ordering as Knuth_Rule1

from generate_test import generate_probs, generate_fuzz_search, generate_search

from random import shuffle
from BSTTree import BSTTree

def test():

    ##### Try different trees at Huck Finn

    # huck = [word for line in open("test_data/hfinn.txt", 'r') for word in line.split()]
    # (alphas, betas, beta_values) = generate_probs(huck)
    # huck.sort()

    corpus = [word for line in open("test_data/warandpeace.txt", 'r') for word in line.split()]
    corpus = corpus[:100000]
    (alphas, betas, beta_values) = generate_probs(corpus)

    print "CORPUS = WAR AND PEACE\n"
    print "total words:", len(corpus), "keys:", len(beta_values)

    ##generate fuzz search
    num_searches = 42000
    print "Generating test lists..."
    fuzz_search_list = generate_fuzz_search(alphas, betas, num_searches, corpus)
    search_list = generate_search(alphas, betas, num_searches, corpus)
    shuffle(search_list)

    #define number of corpus repeats
    corpus_repeats = 2

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



    exit(1)

    # values = [i for i in range(1000)]
    # start = time.time()
    # (exp, root) = Knuth_find([0.0004997501249] * 1000, [0.0004997501249] * 1001, 1000)
    # tree = Knuth_build(root, values)
    # end = time.time()
    # print "Time to build a Knuth tree of 1000 items:", end-start
    # start = time.time()
    # for x in range(200):
    #     for y in range(1000):
    #         tree.find(y)
    # end = time.time()
    # print "Time to search for all 1000 items 200 times each:", end-start
    # print "average time per lookup:", (end-start) / (200 * 1000)

    # size = 10
    # while size < 11:
    #     total_size = size + size + 1
    #     prob = (float(1) / total_size)
    #     bs = [prob for i in range(size)]
    #     aes= [prob for i in range (size + 1)]
    #     # aes = [a * 100000 for a in aes]
    #     # bs  = [b * 100000 for b in bs]
    #     print "building tree of", size
    #     print bs[0], aes[0], len(bs), len(aes)
    #     tree = Nlogn_build(bs, aes, size, [i for i in range(size)])
    #     print tree
    #     itms = []
    #     tree.inorder_traversal(lambda x : itms.append(x))
    #     print "size is %d and items length is %d" % (size, len(itms))
    #     if len(itms) != size:
    #         # print bs
    #         # print aes
    #         print size
    #         # print [i for i in range(size)]
    #         print tree
    #         exit(1)
    #     size += 1
    # exit(1)

    ### Try building a probability distribution of word frequency of 
    ### Huckleberry Finn
    # sys.setrecursionlimit(2000)
    huck = [word for line in open("test_data/hfinn.txt", 'r') for word in line.split()]
    # huck.sort()
    (alphas, betas, beta_values) = generate_probs(huck)
    # alphas = [0.0 for a in alphas]
    # alphas = [a * 100000 for a in alphas]
    # betas  = [b * 100000 for b in betas]
    print len(alphas), len(betas), len(beta_values)
    tree = Nlogn_build(betas, alphas, len(betas), beta_values, min(betas) / 2)
    print tree
    # tree.inorder_traversal_iter(lambda x : sys.stdout.write(x + "\n"))
    exit(1)
    # tree.inorder_traversal_iter(lambda x : x)
    itms = []
    tree.inorder_traversal(lambda x : itms.append(x))
    print "length is %d" % (len(itms))
    exit(1)
    # print beta_values[:300]
    (exp, root) = Knuth_find(betas, alphas, len(betas))
    tree = Knuth_build(root, beta_values)
    # print tree

    exit(1)

    # size = 1
    # while size < 2000:
    #     total_size = size + size + 1
    #     prob = (float(1) / total_size)
    #     bs = [prob for i in range(size)]
    #     aes= [prob for i in range (size + 1)]
    #     # aes = [a * 100000 for a in aes]
    #     # bs  = [b * 100000 for b in bs]
    #     print "building tree of", size
    #     print bs[0], aes[0], len(bs), len(aes)
    #     tree = Nlogn_build(bs, aes, size, [i for i in range(size)])
    #     print tree
    #     itms = []
    #     tree.inorder_traversal(lambda x : itms.append(x))
    #     print "size is %d and items length is %d" % (size, len(itms))
    #     if len(itms) != size:
    #         # print bs
    #         # print aes
    #         print size
    #         # print [i for i in range(size)]
    #         print tree
    #         exit(1)
    #     size += 1
    # exit(1)

    size = 1000
    total_size = size + size + 1
    prob = (float(1) / total_size)
    bs = [prob for i in range(size)]
    aes= [prob for i in range (size + 1)]
    values = [i for i in range(size)]
    shuffle(values)
    # print bs[0], aes[0], len(bs), len(aes)
    start = time.time()
    t = BSTTree(None)
    for v in values:
        t.insert(v)
    end = time.time()
    print "Time to build naive tree:", end-start
    start = time.time()
    for x in range(200):
        for y in range(1000):
            t.find(y)
    end = time.time()
    print "Time to search for all 1000 items 200 times each:", end-start
    print "average time per lookup:", (end-start) / (200 * 1000)
    exit(1)
    # tree = Nlogn_build(bs, aes, size, [i for i in range(size)])
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
    exit(1)

    # values = [i for i in range(1000)]
    # start = time.time()
    # (exp, root) = Knuth_n3_find([0.0004997501249] * 1000, [0.0004997501249] * 1001, 1000)
    # tree = Knuth_n3_build(root, values)
    # end = time.time()
    # print "Time to build a Knuth tree of 1000 items:", end-start
    # start = time.time()
    # for x in range(200):
    #     for y in range(1000):
    #         tree.find(y)
    # end = time.time()
    # print "Time to search for all 1000 items 200 times each:", end-start
    # print "average time per lookup:", (end-start) / (200 * 1000)
    # exit(1)

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
    exit(1)

    size = 10000
    while size < 10001:
        total_size = size + size + 1
        prob = (float(1) / total_size)
        bs = [prob for i in range(size)]
        aes= [prob for i in range (size + 1)]
        print "building tree of", size
        print bs[0], aes[0], len(bs), len(aes)
        tree = Nlogn_build(bs, aes, size, [i for i in range(size)])
        # print tree
        itms = []
        tree.inorder_traversal(lambda x : itms.append(x))
        print "size is %d and items length is %d" % (size, len(itms))
        if len(itms) != size:
            # print bs
            # print aes
            print size
            # print [i for i in range(size)]
            print tree
            exit(1)
        size += 1
    exit(1)

    ### Try building a probability distribution of word frequency of 
    ### Huckleberry Finn
    # sys.setrecursionlimit(2000)
    huck = [word for line in open("test_data/hfinn.txt", 'r') for word in line.split()]
    huck.sort()
    (alphas, betas, beta_values) = generate_probs(huck)
    # alphas = [0.0 for a in alphas]
    alphas = [a * 100000 for a in alphas]
    betas  = [b * 100000 for b in betas]
    print sum(betas) + sum(alphas)
    # exit(1)
    print len(alphas), len(betas), len(beta_values)
    tree = Nlogn_build(betas, alphas, len(betas), beta_values)
    # print tree
    # tree.inorder_traversal_iter(lambda x : sys.stdout.write(x + "\n"))
    exit(1)
    # tree.inorder_traversal_iter(lambda x : x)
    itms = []
    tree.inorder_traversal(lambda x : itms.append(x))
    print "length is %d" % (len(itms))
    exit(1)
    # print beta_values[:300]
    (exp, root) = Knuth_find(betas, alphas, len(betas))
    tree = Knuth_build(root, beta_values)
    print tree

    exit(1)
    # values = [i for i in range(1000)]
    # start = time.time()
    # (exp, root) = Knuth_find([0.0004997501249] * 1000, [0.0004997501249] * 1001, 1000)
    # tree = Knuth_build(root, values)
    # end = time.time()
    # print "Time to build a Knuth tree of 1000 items:", end-start
    # start = time.time()
    # for x in range(200):
    #     for y in range(1000):
    #         tree.find(y)
    # end = time.time()
    # print "Time to search for all 1000 items 200 times each:", end-start
    # print "average time per lookup:", (end-start) / (200 * 1000)

    values = [i for i in range(1000)]
    start = time.time()
    # tree = Nlogn_build([0.000499750124938] * 1000, [0.000499750124938] * 1001, 1000, values)
    # tree = Nlogn_build([0.2, 0.2, 0.2, 0.2], [0.04, .04, .04, .04, .04], 4, [i for i in range(4)])
    # print tree
    size = 1
    while size < 2000:
        total_size = size + size + 1
        prob = float(1) / total_size
        bs = [prob for i in range(size)]
        aes= [prob for i in range (size + 1)]
        print "building tree of", size
        print bs[0], aes[0], len(bs), len(aes)
        tree = Nlogn_build(bs, aes, size, [i for i in range(size)])
        print tree
        print
        print

        itms = []
        tree.inorder_traversal(lambda x : itms.append(x))
        print "size is %d and items length is %d" % (size, len(itms))
        if len(itms) != size:
            # print bs
            # print aes
            print size
            # print [i for i in range(size)]
            print tree
            exit(1)
        size += 1
    exit(1)


    exit(1)
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