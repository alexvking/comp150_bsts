# optimal_bst_knuth.py
# COMP 150
# Created by Cori Jacoby and Alex King
# 4/9/2017

# Implementation of Knuth's O(n^2) algorithm for optimal
# binary search trees

import sys
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
        if y % 500 == 0:
            print "Knuth algorithm: on iteration", y, "of", beta_len + 1
        for i in range(beta_len - y):
            j = i + y + 1
            exp_table[i][j] = float("inf")
            weight_table[i][j] = weight_table[i][j - 1] + beta_list[j - 1] + alpha_list[j]

            l_index = i
            r_index = j

            #check if left index is one off of right index - if so only one root
            #else reset using speedup and j is - 1 more every time because of
            #indexing disconnect and we have to add 1 to r_index so its inclusive
            if l_index + 1 != r_index:
                l_index = root_table[i][j - 2]
                r_index = root_table[i + 1][j - 1] + 1
            for root in range(l_index, r_index):
                
                t = exp_table[i][root] + exp_table[root + 1][j] + weight_table[i][j]

                if t < exp_table[i][j]:
                    exp_table[i][j] = t
                    root_table[i][j - 1] = root

    return (exp_table, root_table)

# construct_tree : root_table -> list of indices
# in case of building tree, must pass in k_list so that actual values can be inserted
def construct_tree(root_table):
    (i, j) = 0, len(root_table) - 1
    node_stack = [(i, j)] # parent
    element_list = []
    while node_stack:
        (i, j) = node_stack.pop()
        print i, j
        next_root = root_table[i][j]
        element_list.append(next_root)
        if (next_root + 1 <= j):
            node_stack.append((next_root + 1, j))
        if i <= (next_root - 1):
            node_stack.append((i, next_root - 1))
            
    return element_list

# construct_tree : root_table -> BSTTree
def construct_tree_inline(root_table, key_list):
    (i, j) = 0, len(root_table) - 1
    root_index = root_table[i][j]
    root = BSTTree(key_list[root_index])
    node_stack = []
    if (root_index + 1 <= j):
        node_stack.append((root_index + 1, j, root))
    if i <= (root_index - 1):
        node_stack.append((i, root_index - 1, root))

    while node_stack:
        (i, j, parent) = node_stack.pop()
        next_root = root_table[i][j]
        node = BSTTree(key_list[next_root])
        if node.value < parent.value:
            parent.left = node
        else:
            parent.right = node

        if (next_root + 1 <= j):
            node_stack.append((next_root + 1, j, node))
        if i <= (next_root - 1):
            node_stack.append((i, next_root - 1, node))
            
    return root


def print_table(table):
    for row in table:
        print row

def print_value(x):
    sys.stdout.write(str(x) + "\n")