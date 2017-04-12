# optimal_bst_knuth.py
# COMP 150
# Created by Cori Jacoby and Alex King
# 4/9/2017

# Implementation of Knuth's O(n^3) algorithm for optimal
# binary search trees

from BSTTree import BSTTree

def find_optimal_tree_ordering(beta_list, alpha_list, beta_len):
    #initialize 2D arrays
    exp_table = [[None for i in range(beta_len + 1)] 
                  for j in range(1, beta_len + 2)]
    weight_table = [[None for i in range(beta_len + 1)] 
                  for j in range(1, beta_len + 2)]
    root_table = [[None for i in range(beta_len)] for j in range(beta_len)]

    for x in range(beta_len + 1):
        exp_table[x][x] = alpha_list[x]
        weight_table[x][x] = alpha_list[x]

    for y in range(beta_len + 1): 
        for i in range(beta_len - y):
            j = i + y + 1
            #print "accessing exp: [%i][%i]" %(i, j)
            exp_table[i][j] = float("inf")
            #print "exp_table: \n", print_table(exp_table)
            weight_table[i][j] = weight_table[i][j - 1] + beta_list[j - 1] + alpha_list[j]
            #print "\nweight_table: \n", print_table(weight_table)

            for root in range(i, j):

                #print exp_table[i][root], exp_table[root + 1][j], weight_table[i][j]
                t = exp_table[i][root] + exp_table[root + 1][j] + weight_table[i][j]

                if t < exp_table[i][j]:
                    exp_table[i][j] = t
                    root_table[i][j - 1] = root
                    #print "exp_table: after updating at ij\n", print_table(exp_table)
                    #print "\nroot_table: \n", print_table(root_table)

    #print "exp_table: \n", print_table(exp_table)
    #print "root_table: \n", print_table(root_table)
    return (exp_table, root_table)

def print_table(table):
    for row in table:
        print row

def test():
    #find_optimal_tree_ordering([.1], [.45, .45], 1)
    #find_optimal_tree_ordering([0.00004999750012] * 10000, [0.00004999750012] * 10001, 10000)
    find_optimal_tree_ordering([0.0004997501249] * 1000, [0.0004997501249] * 1001, 1000)

test()
